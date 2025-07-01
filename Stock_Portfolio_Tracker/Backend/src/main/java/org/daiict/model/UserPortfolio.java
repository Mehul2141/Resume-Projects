package org.daiict.model;

import lombok.Data;

import javax.persistence.*;
import java.util.Date;

@Entity
@Data
public class UserPortfolio {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private UserDetail userDetail;

    @ManyToOne
    @JoinColumn(name = "stock_id", nullable = false)
    private StockData stockData;

    private Float purchasePrice;
    private Float amount;
    private Float totalValue;
    private Float changeAmount;
    private Float changePercent;
    private Date purchaseDate;
}
