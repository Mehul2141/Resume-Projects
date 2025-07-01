package org.daiict.service;


import org.daiict.model.UserDetail;

public interface UserService {

    public UserDetail createUser(UserDetail user);

    public boolean checkEmail(String email);

}
