package org.daiict.controller;

import org.daiict.auth.JwtResponse;
import org.daiict.auth.JwtUtils;
import org.daiict.auth.LoginRequest;
import org.daiict.config.CustomUserDetails;
import org.daiict.model.UserDetail;
import org.daiict.repository.UserRepository;
import org.daiict.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpSession;
import java.security.Principal;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Controller
@RestController
public class UserController {
    @Autowired
    AuthenticationManager authenticationManager;

    @Autowired
    UserRepository userRepository;

    @Autowired
    PasswordEncoder encoder;

    @Autowired
    private UserService userService;

    @Autowired
    JwtUtils jwtUtils;

    @PostMapping("/register")
    public ResponseEntity<UserDetail> createUser(@RequestBody UserDetail user) {
        boolean f = userService.checkEmail(user.getEmail());
        if (f) {
            return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
        } else {
            UserDetail userDetail = userService.createUser(user);
            return new ResponseEntity<>(userDetail, HttpStatus.OK);
        }
    }

    @PostMapping("/login")
    public ResponseEntity<JwtResponse> authenticateUser(@RequestBody LoginRequest loginRequest) {
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(loginRequest.getUsername(), loginRequest.getPassword()));
        SecurityContextHolder.getContext().setAuthentication(authentication);
        String jwt = jwtUtils.generateJwtToken(authentication);
        CustomUserDetails userDetails = (CustomUserDetails) authentication.getPrincipal();
        List<String> roles = userDetails.getAuthorities().stream().map(GrantedAuthority::getAuthority).collect(Collectors.toList());
        return ResponseEntity.ok(new JwtResponse(jwt,
                userDetails.getUsername(),
                roles));
    }

    @GetMapping("/user/detail")
    public ResponseEntity<UserDetail> getUser(@RequestParam String username) {
        return ResponseEntity.ok(userRepository.findByEmail(username));
    }

}
