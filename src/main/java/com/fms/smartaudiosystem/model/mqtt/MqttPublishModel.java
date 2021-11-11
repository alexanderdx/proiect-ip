package com.fms.smartaudiosystem.model.mqtt;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import lombok.Data;

/**
 * Class for storing and validating MQTT messages
 */
@Data
public class MqttPublishModel {

    @NotNull
    @Size(min = 1, max = 255)
    private String topic;

    @NotNull
    @Size(min = 1, max = 255)
    private String message;

    @NotNull
    private Boolean retained;

    @NotNull
    private Integer qos;
}
