package com.fms.smartaudiosystem.model;

import javax.validation.constraints.NotNull;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document
public class User {
    @Id
    private long id;

    @NotNull
    private String name;

    public User(String name) {
        this.name = name;
    }
}
