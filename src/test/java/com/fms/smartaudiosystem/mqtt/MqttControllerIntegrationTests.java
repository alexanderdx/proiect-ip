package com.fms.smartaudiosystem.mqtt;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fms.smartaudiosystem.model.mqtt.MqttPublishModel;
import com.fms.smartaudiosystem.model.mqtt.MqttSubscribeModel;
import com.fms.smartaudiosystem.route.MqttController;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

@WebMvcTest(controllers = MqttController.class)
public class MqttControllerIntegrationTests {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    public void testInvalidMqttMessageReturns400() throws Exception {
        MqttPublishModel message = new MqttPublishModel();
        message.setMessage(null);
        message.setTopic(null);
        message.setQos(null);
        message.setRetained(null);

        mockMvc.perform(
                post("/mqtt/publish")
                    .contentType("application/json")
                    .content(objectMapper.writeValueAsString(message)))
                .andExpect(status().isBadRequest());
    }

    @Test
    public void testValidMqttMessageIsPublished() throws Exception {
        MqttPublishModel message = new MqttPublishModel();
        message.setMessage("Test Valid MQTT Message Is Published");
        message.setTopic("testValidMqttMessageIsPublished");
        message.setQos(0);
        message.setRetained(false);

        mockMvc.perform(
                post("/mqtt/publish")
                    .contentType("application/json")
                    .content(objectMapper.writeValueAsString(message)))
                .andExpect(status().isOk());
    }

    @Test
    public void testExpectedMessageIsRetrieved() throws Exception {
        MqttPublishModel message = new MqttPublishModel();
        message.setMessage("Test Expected Message Is Retrieved");
        message.setTopic("testExpectedMessageIsRetrieved");
        message.setQos(0);
        message.setRetained(true);

        mockMvc.perform(
                post("/mqtt/publish")
                    .contentType("application/json")
                    .content(objectMapper.writeValueAsString(message)))
                .andExpect(status().isOk());

        MvcResult response = mockMvc.perform(
                get("/mqtt/subscribe")
                    .param("topic", message.getTopic()))
                .andExpect(status().isOk())
                .andReturn();

        String json = response.getResponse().getContentAsString();
        MqttSubscribeModel responseMessage = objectMapper.readValue(json, MqttSubscribeModel.class);

        assertEquals(message.getMessage(), responseMessage.getMessage());
        assertEquals(message.getQos(), responseMessage.getQos());
    }
}
