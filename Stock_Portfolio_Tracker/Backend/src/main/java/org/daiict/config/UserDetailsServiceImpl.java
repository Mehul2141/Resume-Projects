package org.daiict.config;

import org.daiict.model.UserDetail;
import org.daiict.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

@Service
public class UserDetailsServiceImpl implements UserDetailsService {

    @Autowired
    private UserRepository userRepository;

    @Override
    public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {

        UserDetail user = userRepository.findByEmail(email);
        if(user==null)
        {
            throw new UsernameNotFoundException("user not available");
        }

        return new CustomUserDetails(user);
    }
}
