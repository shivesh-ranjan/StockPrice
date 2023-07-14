package com.example.stockprediction;

import java.util.Map;

public class AlphaVantageResponse {
    private Map<String, AlphaVantageData> timeSeries;

    public Map<String, AlphaVantageData> getTimeSeries() {
        return timeSeries;
    }

    public void setTimeSeries(Map<String, AlphaVantageData> timeSeries) {
        this.timeSeries = timeSeries;
    }
}
