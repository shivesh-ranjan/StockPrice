package com.example.stockprediction;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
public class StockDataCollector {

    @Value("${api.key}") // Externalize the API key as a configuration property
    private String apiKey;

    private RestTemplate restTemplate = new RestTemplate();

    private final KafkaTemplate<String, StockPrice> kafkaTemplate;
    private final String kafkaTopic;

    public StockDataCollector(KafkaTemplate<String, StockPrice> kafkaTemplate, @Value("${kafka.topic}") String kafkaTopic) {
        this.kafkaTemplate = kafkaTemplate;
        this.kafkaTopic = kafkaTopic;
    }

    @Scheduled(fixedDelay = 60000) // Run the data collection every 60 seconds
    public void collectData() {
        String symbol = "AAPL"; // Replace with the desired stock symbol

        // Make API request to retrieve real-time stock price data from Alpha Vantage
        String apiUrl = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + symbol + "&interval=1min&apikey=" + apiKey;
        AlphaVantageResponse response = restTemplate.getForObject(apiUrl, AlphaVantageResponse.class);

        if (response != null && response.getTimeSeries() != null) {
            // Process and preprocess the retrieved data
            for (String timestamp : response.getTimeSeries().keySet()) {
                AlphaVantageData data = response.getTimeSeries().get(timestamp);

                // Handle missing values
                if (data.getClose() != null && !data.getClose().isEmpty()) {
                    double closePrice = Double.parseDouble(data.getClose());
                    
                    // Create StockPrice object
                    StockPrice stockPrice = new StockPrice(symbol, timestamp, closePrice);

                    // Publish the stock price data to the Kafka topic
                    kafkaTemplate.send(kafkaTopic, stockPrice);
                }
            }

            System.out.println("Data collection and preprocessing executed!");
        } else {
            System.out.println("Failed to retrieve stock price data from Alpha Vantage.");
        }
    }
}
