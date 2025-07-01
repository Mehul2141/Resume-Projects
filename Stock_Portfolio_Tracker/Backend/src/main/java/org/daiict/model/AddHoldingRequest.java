package org.daiict.model;

import lombok.Data;
import java.util.Date;

@Data
public class AddHoldingRequest {
    String symbol;
    Float amount;
    Float purchasePrice;
    Date purchaseDate;
}
