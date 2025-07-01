package org.daiict.service;

import com.fasterxml.jackson.databind.JsonNode;
import org.daiict.config.ConfigProperties;
import org.daiict.model.CompanyDetail;
import org.daiict.model.QuoteResponse;
import org.daiict.model.SearchStockResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.ArrayList;
import java.util.List;

@Service
public class StockDataService {
    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    private ConfigProperties configProperties;

    public QuoteResponse.QuoteData getStockQuote(String symbol) {
        try {
            String url = String.format("https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=%s&apikey=%s", symbol, configProperties.getAlphaVantageApiKey());
            QuoteResponse response = restTemplate.getForObject(url, QuoteResponse.class);
            return response.getQuoteData();
        }catch (Exception e){
            e.printStackTrace();
        }
        // returning empty QuoteData if fetch fails
        return new QuoteResponse.QuoteData();
    }

    public List<SearchStockResponse.SearchStockResponseData> searchStock(String query) {
        try {
            String url = String.format("https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=%s&apikey=%s", query, configProperties.getAlphaVantageApiKey());
            SearchStockResponse searchStockResponse = restTemplate.getForObject(url, SearchStockResponse.class);
            return searchStockResponse.getBestMatches();
        } catch (Exception e) {
            e.printStackTrace();
        }
        // returning empty list if search fails
        return new ArrayList<>();
    }

    public CompanyDetail getCompanyDetail(String symbol) {
        try {
            String url = String.format("https://www.alphavantage.co/query?function=OVERVIEW&symbol=%s&apikey=%s", symbol, configProperties.getAlphaVantageApiKey());
            CompanyDetail companyDetail = restTemplate.getForObject(url, CompanyDetail.class);
            return companyDetail;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return new CompanyDetail();
    }

    public Double getSMA(String symbol) {
        try {
            String url = String.format("https://www.alphavantage.co/query?function=SMA&symbol=%s&interval=weekly&time_period=10&series_type=open&apikey=%s", symbol, configProperties.getAlphaVantageApiKey());
            JsonNode response = restTemplate.getForObject(url, JsonNode.class);
            JsonNode technicalData = response.get("Technical Analysis: SMA");
            JsonNode sma = technicalData.fields().next().getValue();
            return  sma.get("SMA").asDouble();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return -1.0D;
    }

    public Double getMACD(String symbol) {
        try {
            String url = String.format("https://www.alphavantage.co/query?function=MACDEXT&symbol=%s&interval=daily&series_type=open&apikey=%s", symbol, configProperties.getAlphaVantageApiKey());
            JsonNode response = restTemplate.getForObject(url, JsonNode.class);
            JsonNode technicalData = response.get("Technical Analysis: MACDEXT");
            JsonNode sma = technicalData.fields().next().getValue();
            return  sma.get("MACD").asDouble();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return -1.0D;
    }

    public Double getRSI(String symbol) {
        try {
            String url = String.format("https://www.alphavantage.co/query?function=RSI&symbol=%s&interval=weekly&time_period=10&series_type=open&apikey=%s", symbol, configProperties.getAlphaVantageApiKey());
            JsonNode response = restTemplate.getForObject(url, JsonNode.class);
            JsonNode technicalData = response.get("Technical Analysis: RSI");
            JsonNode sma = technicalData.fields().next().getValue();
            return  sma.get("RSI").asDouble();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return -1.0D;
    }
}
