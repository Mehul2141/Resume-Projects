package org.daiict.service;

import org.daiict.model.*;
import org.daiict.repository.CompanyDetailRepository;
import org.daiict.repository.StockDataRepository;
import org.daiict.repository.UserPortfolioRepository;
import org.daiict.repository.UserRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import javax.transaction.Transactional;
import java.util.List;

@Component
public class UserPortfolioService {

    @Autowired
    private StockDataRepository stockDataRepository;

    @Autowired
    private UserPortfolioRepository userPortfolioRepository;

    @Autowired
    private StockDataService stockDataService;

    @Autowired
    private CompanyDetailRepository companyDetailRepository;

    @Autowired
    private UserRepository userRepository;

    private static final Logger log = LoggerFactory.getLogger(UserPortfolioService.class);

    public UserPortfolio saveHolding(AddHoldingRequest addHoldingRequest, String userId) {
        StockData stockData = getOrCrateStockDataEntity(addHoldingRequest.getSymbol());
        UserDetail userDetail = userRepository.findByEmail(userId);
        UserPortfolio userPortfolio = userPortfolioRepository.findFirstByUserDetailAndStockData(userDetail, stockData);
        if (userPortfolio == null) {
            userPortfolio = new UserPortfolio();
        }
        userPortfolio.setStockData(stockData);
        userPortfolio.setUserDetail(userDetail);
        userPortfolio.setAmount(addHoldingRequest.getAmount());
        userPortfolio.setPurchasePrice(addHoldingRequest.getPurchasePrice());
        Float change = stockData.getPrice() - addHoldingRequest.getPurchasePrice();
        Float changePercent = (change * 100f) / addHoldingRequest.getPurchasePrice();
        userPortfolio.setChangeAmount(change);
        userPortfolio.setChangePercent(changePercent);
        userPortfolio.setTotalValue(addHoldingRequest.getAmount() * addHoldingRequest.getPurchasePrice());
        userPortfolio.setPurchaseDate(addHoldingRequest.getPurchaseDate());
        return userPortfolioRepository.save(userPortfolio);
    }

    @Transactional
    public void removeHolding(String symbol, String userId) {
        UserDetail userDetail = userRepository.findByEmail(userId);
        StockData stockData = stockDataRepository.findFirstBySymbol(symbol);
        userPortfolioRepository.deleteUserPortfolioByUserDetailAndStockData(userDetail, stockData);
    }

    private StockData getOrCrateStockDataEntity(String symbol) {
        StockData stockData = stockDataRepository.findFirstBySymbol(symbol);
        if (stockData == null) {
            log.info("Stock data not present, creating stock data entity");
            QuoteResponse.QuoteData quoteData = stockDataService.getStockQuote(symbol);
            CompanyDetail companyDetail = stockDataService.getCompanyDetail(symbol);
            try {
                companyDetailRepository.save(companyDetail);
            }catch (Exception e){
                e.printStackTrace();
            }
            Double macd = stockDataService.getMACD(symbol);
            Double rsi = stockDataService.getRSI(symbol);
            Double sma = stockDataService.getSMA(symbol);
            stockData = new StockData();
            stockData.setSymbol(symbol);
            stockData.setPrice(quoteData.getPrice());
            stockData.setOpen(quoteData.getOpen());
            stockData.setHigh(quoteData.getHigh());
            stockData.setLow(quoteData.getLow());
            stockData.setVolume(quoteData.getVolume());
            stockData.setLatestTradingDay(quoteData.getLatestTradingDay());
            stockData.setPreviousClose(quoteData.getPreviousClose());
            stockData.setChangeValue(quoteData.getChange());
            stockData.setChangePercent(quoteData.getChangePercent());
            stockData.setMacd(macd);
            stockData.setRsi(rsi);
            stockData.setSma(sma);
            return stockDataRepository.save(stockData);
        }
        return stockData;
    }

    public List<UserPortfolio> getUserPortfolio(String userId){
        UserDetail userDetail = userRepository.findByEmail(userId);
        return userPortfolioRepository.findAllByUserDetail(userDetail);
    }

}
