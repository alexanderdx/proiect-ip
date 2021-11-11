package com.fms.smartaudiosystem.hub;

import static com.fms.smartaudiosystem.Application.log;
import static com.fms.smartaudiosystem.utils.Constants.MQTT_SERVER_ADDRES;
import static com.fms.smartaudiosystem.utils.Constants.TEST_TOPIC;

import com.fms.smartaudiosystem.model.mqtt.MqttPublishModel;
import com.fms.smartaudiosystem.mqtt.MqttClient;
import java.sql.Array;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import javax.validation.constraints.NotNull;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttMessage;

public class CentralHub implements MqttCallback {

    private static final String MQTT_PUBLISHER_ID = "central-hub";

    @NotNull
    private final MqttClient mqttClient;

    private final List<ChildHub> childHubList;

    CentralHub() {
        log.info("Initializing central hub...");
        mqttClient = new MqttClient(MQTT_SERVER_ADDRES, MQTT_PUBLISHER_ID);
        mqttClient.setCallback(this);
        mqttClient.subscribe(TEST_TOPIC);

        childHubList = new ArrayList<>();
        spawnChildHubs();
    }

    private static class SingletonHolder {

        private static final CentralHub INSTANCE = new CentralHub();
    }

    public static CentralHub getInstance() {
        return SingletonHolder.INSTANCE;
    }

    public void spawnChildHubs() {
        log.info("Spawning child hubs...");

        for (int i = 0; i < 5; ++i)
            childHubList.add(new ChildHub(i));
    }

    public void publishMessage(MqttPublishModel message) {
        mqttClient.publishMessage(message);
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
}
