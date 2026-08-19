package services;

import repositories.UserRepository;
import java.util.List;

public class UserService {

    private final UserRepository repository;

    public UserService(UserRepository repository) {
        this.repository = repository;
    }

    public void createUser() {
        repository.save();
    }
}