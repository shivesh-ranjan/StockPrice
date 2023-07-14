package com.example.stockprediction;

public class StockPrice {
    private String symbol;
    private String timestamp;
    private double price;

    public StockPrice(String symbol, String timestamp, double price) {
        this.symbol = symbol;
        this.timestamp = timestamp;
        this.price = price;
    }

    // Getters and setters (or use Lombok annotations)
}
