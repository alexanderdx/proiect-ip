package com.fms.smartaudiosystem.model.mqtt;

import lombok.Data;

/**
 * Class for storing MQTT subscription responses
 */
@Data
public class MqttResponseModel {

    private String message;
    private Integer qos;
    private Integer id;
}
