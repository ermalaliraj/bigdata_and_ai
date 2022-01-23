package org.ea.oj.service;

import org.junit.Before;
import org.junit.Ignore;
import org.junit.Rule;
import org.junit.rules.Timeout;
import org.junit.runner.RunWith;
import org.mockito.MockitoAnnotations;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import java.util.concurrent.TimeUnit;

@Ignore
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {"classpath:servicesContext.xml"})
public class AbstractSpringTest {

//    @Rule
//    public Timeout timeout = new Timeout(60, TimeUnit.SECONDS);

    @Before
    public void setup() {
        MockitoAnnotations.initMocks(this);
    }
}
