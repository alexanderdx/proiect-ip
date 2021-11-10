package com.fms.smartaudiosystem.mqtt;

import static com.fms.smartaudiosystem.Application.log;

import org.eclipse.paho.client.mqttv3.IMqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;


public class MqttClient {

    private static final String MQTT_PUBLISHER_ID = "central-hub";
    private static final String MQTT_SERVER_ADDRES = "tcp://127.0.0.1:1883";
    private static IMqttClient instance;

    public static IMqttClient getInstance() {
        try {
            if (instance == null) {
                log.info(String.format("Instantiating MQTT client at %s", MQTT_SERVER_ADDRES));
                instance = new org.eclipse.paho.client.mqttv3.MqttClient(MQTT_SERVER_ADDRES,
                        MQTT_PUBLISHER_ID);
            }

            MqttConnectOptions options = new MqttConnectOptions();
            options.setAutomaticReconnect(true);
            options.setCleanSession(true);
            options.setConnectionTimeout(10);

            if (!instance.isConnected()) {
                instance.connect(options);
            }
        } catch (MqttException e) {
            e.printStackTrace();
        }

        return instance;
    }

    public static void disconnect() {
        try {
            if (instance.isConnected()) {
                instance.disconnect();
            }
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    private MqttClient() {

    }
}

