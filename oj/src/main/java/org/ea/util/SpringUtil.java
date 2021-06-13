package org.ea.util;

import org.springframework.context.support.ClassPathXmlApplicationContext;

public class SpringUtil {
    public static <T> T getBeanFromSpring(String beanName) {
        ClassPathXmlApplicationContext applicationContext = new ClassPathXmlApplicationContext(
                new String[] { "classpath*:**//servicesContext.xml" });

        @SuppressWarnings("unchecked")
        T object = (T) applicationContext.getBean(beanName);
        return object;
    }
}
