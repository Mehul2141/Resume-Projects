package org.daiict.repository;

import org.daiict.model.StockData;
import org.daiict.model.UserDetail;
import org.daiict.model.UserPortfolio;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface UserPortfolioRepository extends JpaRepository<UserPortfolio, Integer> {

    UserPortfolio findFirstByUserDetailAndStockData(UserDetail user, StockData stockData);

    void deleteUserPortfolioByUserDetailAndStockData(UserDetail user, StockData stockData);

    List<UserPortfolio> findAllByUserDetail(UserDetail userDetail);

}
