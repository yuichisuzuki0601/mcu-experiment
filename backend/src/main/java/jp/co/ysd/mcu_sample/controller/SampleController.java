package jp.co.ysd.mcu_sample.controller;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Map;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping
public class SampleController {

    private static final DateTimeFormatter DTF = DateTimeFormatter.ofPattern("yyyy/MM/dd(E) HH:mm:ss", Locale.JAPANESE);

    private List<String> histories = new ArrayList<>();

    @GetMapping
    public List<String> get() {
        return histories;
    }

    @PostMapping
    public Map<String, String> post(@RequestBody String data) {
        var history = LocalDateTime.now().format(DTF) + " " + data;
        System.out.println(history);
        histories.add(history);
        // TODO 楽天APIにバーコードを投げて結果を受け取りたい
        // https://webservice.rakuten.co.jp/explorer/api/Product/Search
        return Map.of("status", "OK");
    }

    @GetMapping("clear")
    public List<String> clear() {
        histories.clear();
        return histories;
    }

}
