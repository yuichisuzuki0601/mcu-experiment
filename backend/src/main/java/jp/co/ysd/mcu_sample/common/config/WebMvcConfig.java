package jp.co.ysd.mcu_sample.common.config;

import java.util.Collections;
import java.util.stream.Collectors;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@Configuration
public class WebMvcConfig implements WebMvcConfigurer {

    private HandlerInterceptor commonInterceptor = new HandlerInterceptor() {
        @Override
        public boolean preHandle(HttpServletRequest req, HttpServletResponse res, Object h) {
            var headers = Collections.list(req.getHeaderNames()).stream()
                    .collect(Collectors.toMap(name -> name, name -> req.getHeader(name)));
            IO.println(headers);
            return true;
        }
    };

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(commonInterceptor);
    }

}
