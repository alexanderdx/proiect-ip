package com.fms.smartaudiosystem.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.BAD_REQUEST)
public class MqttParameterException extends RuntimeException {

    public MqttParameterException(String message) {
        super(message);
    }
}
