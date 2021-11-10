package com.fms.smartaudiosystem.route;

import static com.fms.smartaudiosystem.Application.log;

import com.fms.smartaudiosystem.exception.MqttParameterException;
import com.fms.smartaudiosystem.model.mqtt.MqttPublishModel;
import com.fms.smartaudiosystem.model.mqtt.MqttSubscribeModel;
import com.fms.smartaudiosystem.mqtt.MqttClient;
import javax.validation.Valid;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping(value = "/mqtt")
public class MqttController {

    @PostMapping("publish")
    public String publishMessage(@RequestBody @Valid MqttPublishModel messagePublishModel,
                                 BindingResult bindingResult) throws MqttException {

        if (bindingResult.hasErrors()) {
            throw new MqttParameterException("MQTT parameters contain errors!");
        }

        MqttMessage mqttMessage = new MqttMessage(messagePublishModel.getMessage().getBytes());
        mqttMessage.setQos(messagePublishModel.getQos());
        mqttMessage.setRetained(messagePublishModel.getRetained());

        MqttClient.getInstance().publish(messagePublishModel.getTopic(), mqttMessage);

        log.info(String.format("Published message '%s' to topic '%s'",
                messagePublishModel.getMessage(), messagePublishModel.getTopic()));

        return "Successfully published message";
    }

    @GetMapping("subscribe")
    public MqttSubscribeModel subscribeChannel(@RequestParam(value = "topic") String topic)
            throws InterruptedException, MqttException {

        MqttSubscribeModel mqttSubscribeModel = new MqttSubscribeModel();

        MqttClient.getInstance().subscribeWithResponse(topic, (s, mqttMessage) -> {
            mqttSubscribeModel.setId(mqttMessage.getId());
            mqttSubscribeModel.setMessage(new String(mqttMessage.getPayload()));
            mqttSubscribeModel.setQos(mqttMessage.getQos());

            log.info(String.format("Received message '%s' from topic '%s'",
                    mqttSubscribeModel.getMessage(), topic));
        });

        return mqttSubscribeModel;
    }
}