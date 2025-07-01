package org.daiict.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class QuoteResponse {
    @JsonProperty("Global Quote")
    private QuoteData quoteData;

    @Getter
    @Setter
    @JsonIgnoreProperties(ignoreUnknown = true)
    public static class QuoteData {
        @JsonProperty("01. symbol")
        private String symbol;
        @JsonProperty("02. open")
        private Float open;
        @JsonProperty("03. high")
        private Float high;
        @JsonProperty("04. low")
        private Float low;
        @JsonProperty("05. price")
        private Float price;
        @JsonProperty("06. volume")
        private Long volume;
        @JsonProperty("07. latest trading day")
        private String latestTradingDay;
        @JsonProperty("08. previous close")
        private Float previousClose;
        @JsonProperty("09. change")
        private Float change;
        @JsonProperty("10. change percent")
        private String changePercent;
    }
}
