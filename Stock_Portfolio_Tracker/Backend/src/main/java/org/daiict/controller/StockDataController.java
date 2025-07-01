package org.daiict.controller;

import org.daiict.config.CustomUserDetails;
import org.daiict.model.*;
import org.daiict.repository.CompanyDetailRepository;
import org.daiict.service.StockDataService;
import org.daiict.service.UserPortfolioService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/stock")
public class StockDataController {
    @Autowired
    private StockDataService stockData;

    @Autowired
    private UserPortfolioService userPortfolioService;

    @Autowired
    private CompanyDetailRepository companyDetailRepository;


    @GetMapping("/quote")
    public QuoteResponse.QuoteData stockData(@RequestParam("symbol") String symbol) {
        return stockData.getStockQuote(symbol);
    }

    @GetMapping("/detail")
    public CompanyDetail getCompanyDetail(@RequestParam("symbol") String symbol) {
        return companyDetailRepository.findById(symbol).get();
    }

    @GetMapping("/search")
    public List<SearchStockResponse.SearchStockResponseData> searchStocks(@RequestParam("query") String query) {
        return stockData.searchStock(query);
    }

    @PostMapping("/add/holding")
    public ResponseEntity<?> addUserHolding(@RequestBody AddHoldingRequest addHoldingRequest) {
        CustomUserDetails userDetails = (CustomUserDetails) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        try {
            UserPortfolio userPortfolio = userPortfolioService.saveHolding(addHoldingRequest, userDetails.getUsername());
            return ResponseEntity.ok(userPortfolio);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return new ResponseEntity<>("Failed to add holding", HttpStatus.INTERNAL_SERVER_ERROR);
    }

    @GetMapping("/remove/holding")
    public ResponseEntity<?> removeUserHolding(@RequestParam("symbol") String symbol) {
        CustomUserDetails userDetails = (CustomUserDetails) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        try {
            userPortfolioService.removeHolding(symbol, userDetails.getUsername());
            return ResponseEntity.ok("deleted");
        } catch (Exception e) {
            e.printStackTrace();
        }
        return new ResponseEntity<>("Failed to delete holding", HttpStatus.INTERNAL_SERVER_ERROR);
    }

    @GetMapping("/portfolio")
    public ResponseEntity<List<UserPortfolio>> getUserPortfolio() {
        CustomUserDetails userDetails = (CustomUserDetails) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        try {
            List<UserPortfolio> userPortfolio = userPortfolioService.getUserPortfolio(userDetails.getUsername());
            return ResponseEntity.ok(userPortfolio);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return new ResponseEntity<>(new ArrayList<>(), HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
