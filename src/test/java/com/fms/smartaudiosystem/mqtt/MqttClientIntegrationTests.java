package com.fms.smartaudiosystem.mqtt;

import static com.fms.smartaudiosystem.Application.log;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.fail;
import static com.fms.smartaudiosystem.utils.Constants.MQTT_SERVER_ADDRES;

import com.fms.smartaudiosystem.model.mqtt.MqttPublishModel;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
public class MqttClientIntegrationTests {

    private static MqttClient sender;

    private static MqttClient receiver;

    @BeforeAll
    static void setup() {
        sender   = new MqttClient(MQTT_SERVER_ADDRES, "test-client-sender");
        receiver = new MqttClient(MQTT_SERVER_ADDRES, "test-client-receiver");
    }

    @Test
    public void testMqttMessageIsPublishedAndRetrieved() {
        // Arrange
        MqttPublishModel message = new MqttPublishModel();
        message.setMessage("Test Valid MQTT Message Is Published");
        message.setTopic("testValidMqttMessageIsPublished");
        message.setQos(0);
        message.setRetained(true);

        receiver.subscribe(message.getTopic());

        // Act
        sender.publishMessage(message);

        // Assert
        try {
            receiver.getClient().subscribeWithResponse(
                    message.getTopic(),
                    (t, msg) -> {
                        assertEquals(message.getMessage(), new String(msg.getPayload()));
                        assertEquals(message.getQos(), msg.getQos());
                    });
        } catch (MqttException e) {
            log.error("Failed to retrieve message");
            e.printStackTrace();
            fail();
        }
    }
}