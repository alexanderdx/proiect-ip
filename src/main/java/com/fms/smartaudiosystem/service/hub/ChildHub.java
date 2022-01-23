package com.fms.smartaudiosystem.service.hub;

import static com.fms.smartaudiosystem.Application.log;
import static com.fms.smartaudiosystem.utils.Constants.MQTT_SERVER_ADDRES;
import static com.fms.smartaudiosystem.utils.Constants.TEST_TOPIC;

import com.fms.smartaudiosystem.mqtt.MqttClient;
import javax.validation.constraints.NotNull;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttMessage;

public class ChildHub implements MqttCallback {

    private final Integer id;

    private String MQTT_PUBLISHER_ID = "child-hub-";

    @NotNull
    private final MqttClient mqttClient;

    public ChildHub(Integer id) {
        log.info(String.format("Initializing child hub %d...", id));
        this.id = id;
        this.MQTT_PUBLISHER_ID += id.toString();

        mqttClient = new MqttClient(MQTT_SERVER_ADDRES, MQTT_PUBLISHER_ID);
        mqttClient.setCallback(this);
        mqttClient.subscribe(TEST_TOPIC);
    }

    @Override
    public void messageArrived(String topic, MqttMessage message) throws Exception {
        log.info(String.format("[%s] Received message from topic '%s': '%s'", MQTT_PUBLISHER_ID,
                topic, new String(message.getPayload())));
    }

    @Override
    public void connectionLost(Throwable cause) {

    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken token) {

    }

    public long getId() {
        return id;
    }
}
