package com.company;

import javax.script.Invocable;
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
import java.io.FileNotFoundException;
import java.io.FileReader;

public class Main {

    public static void main(String[] args) {
        ScriptEngine engine = new ScriptEngineManager().getEngineByName("nashorn");
        try{
            engine.eval("print('Valid access javascript')");
            engine.eval(new FileReader("export_json_data.js"));
            Invocable invocable = (Invocable)engine;
            invocable.invokeFunction("show_data","JavaScript1");
        }catch (ScriptException | FileNotFoundException | NoSuchMethodException e){
            e.printStackTrace();
        }
    }
    public static String show_data(String email,String c_pass ,String n_pass, String re_pass){
        return "Email: "+ email+","+
                "Current Password: " +c_pass +","+
                "New Password: "+ n_pass+","+
                "Retype New Password: "+ re_pass;
    }
}
