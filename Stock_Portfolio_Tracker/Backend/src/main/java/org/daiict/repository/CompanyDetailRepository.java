package org.daiict.repository;

import org.daiict.model.CompanyDetail;
import org.daiict.model.UserPortfolio;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CompanyDetailRepository extends JpaRepository<CompanyDetail, String> {

}
