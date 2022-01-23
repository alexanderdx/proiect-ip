package com.fms.smartaudiosystem.repository;

import com.fms.smartaudiosystem.model.User;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface UserRepository extends MongoRepository<User, String> {

}
