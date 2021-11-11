package com.fms.smartaudiosystem;

import com.fms.smartaudiosystem.hub.CentralHub;
import com.fms.smartaudiosystem.model.mqtt.MqttPublishModel;
import com.fms.smartaudiosystem.mqtt.MqttClient;
import com.fms.smartaudiosystem.utils.Constants;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application implements CommandLineRunner {

    public static final Logger log = LoggerFactory.getLogger(Application.class);

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @Override
    public void run(String... args) throws Exception {
        log.info("Running app...");

        CentralHub centralHub = CentralHub.getInstance();

        // Prepare a message and send it to all children through the central hub
        MqttPublishModel message = new MqttPublishModel();
        message.setMessage("Hello World!");
        message.setTopic(Constants.TEST_TOPIC);
        message.setQos(0);
        message.setRetained(false);

        centralHub.publishMessage(message);
    }
}
