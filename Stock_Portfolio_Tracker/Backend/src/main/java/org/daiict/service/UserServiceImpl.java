package org.daiict.service;

import org.daiict.model.UserDetail;
import org.daiict.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class UserServiceImpl implements UserService{

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private BCryptPasswordEncoder passwordEncoder;

    @Override
    public UserDetail createUser(UserDetail user) {
        user.setPassword(passwordEncoder.encode(user.getPassword()));
        user.setRole("ROLE_USER");
        user.setName(user.getName());
        return userRepository.save(user);

    }

    @Override
    public boolean checkEmail(String email) {
        return userRepository.existsByEmail(email);
    }
}
