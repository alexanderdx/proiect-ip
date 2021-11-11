package com.fms.smartaudiosystem.mqtt;

import static com.fms.smartaudiosystem.Application.log;

import com.fms.smartaudiosystem.model.mqtt.MqttPublishModel;
import com.fms.smartaudiosystem.utils.Constants;
import org.eclipse.paho.client.mqttv3.IMqttClient;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

public class MqttClient {

    private String mqttPublisherId;
    private IMqttClient client;

    public MqttClient() {
        this(Constants.MQTT_SERVER_ADDRES, "default-publisher");
    }

    public MqttClient(String mqttServerAddress, String mqttPublisherId) {
        log.info(String.format("[%s] Instantiating MQTT client", mqttPublisherId));

        try {
            this.client = new org.eclipse.paho.client.mqttv3.MqttClient(mqttServerAddress,
                    mqttPublisherId);
            this.mqttPublisherId = mqttPublisherId;

            MqttConnectOptions options = new MqttConnectOptions();
            options.setAutomaticReconnect(true);
            options.setCleanSession(true);
            options.setConnectionTimeout(10);

            client.connect(options);

        } catch (MqttException e) {
            log.error(String.format("[%s] Failed to instantiate MQTT client", mqttPublisherId));
            e.printStackTrace();
        }
    }

    public void publishMessage(MqttPublishModel messagePublishModel) {
        MqttMessage mqttMessage = new MqttMessage(messagePublishModel.getMessage().getBytes());
        mqttMessage.setQos(messagePublishModel.getQos());
        mqttMessage.setRetained(messagePublishModel.getRetained());

        try {
            client.publish(messagePublishModel.getTopic(), mqttMessage);

            log.info(String.format("[%s] Published message '%s' to topic '%s'", mqttPublisherId,
                    messagePublishModel.getMessage(), messagePublishModel.getTopic()));

        } catch (MqttException e) {
            log.error(String.format("[%s] Failed to publish message to topic '%s'", mqttPublisherId,
                    messagePublishModel.getTopic()));
            e.printStackTrace();
        }
    }

    public void subscribe(String topic) {
        try {
            client.subscribe(topic);

            log.info(String.format("[%s] Subscribed to topic '%s'", mqttPublisherId, topic));

        } catch (MqttException e) {
            log.error(String.format("[%s] Failed to subscribe to topic '%s'", mqttPublisherId,
                    topic));
            e.printStackTrace();
        }
    }

    public IMqttClient getClient() {
        return client;
    }

    public void setCallback(MqttCallback callback) {
        client.setCallback(callback);
    }

    public void disconnect() {
        try {
            if (client.isConnected()) {
                client.disconnect();
            }
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }
}

