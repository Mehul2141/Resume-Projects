package org.daiict.repository;

import org.daiict.model.UserDetail;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<UserDetail,Integer> {

    public boolean existsByEmail(String email);

    public UserDetail findByEmail(String email);
}
