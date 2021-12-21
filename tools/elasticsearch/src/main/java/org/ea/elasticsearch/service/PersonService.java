package org.ea.elasticsearch.service;

import org.ea.elasticsearch.document.Person;
import org.ea.elasticsearch.repository.PersonRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class PersonService {

    private final PersonRepository repository;

    @Autowired
    public PersonService(PersonRepository repository) {
        this.repository = repository;
    }

    public void save(Person person) {
        repository.save(person);
    }

    public Person findById(String id) {
        return repository.findById(id)
                .orElse(null);
    }
}

