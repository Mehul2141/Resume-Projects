package org.daiict.repository;

import org.daiict.model.StockData;
import org.daiict.model.UserPortfolio;
import org.springframework.data.jpa.repository.JpaRepository;

public interface StockDataRepository extends JpaRepository<StockData, Integer> {

    StockData findFirstBySymbol(String symbol);

}
