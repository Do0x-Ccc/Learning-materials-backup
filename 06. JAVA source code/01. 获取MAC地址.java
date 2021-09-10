import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public static String getWindowsMACAddress() {
      String mac = null;
      BufferedReader bufferedReader = null;
      Process process = null;
      try {
         process = Runtime.getRuntime().exec("ipconfig /all");
         bufferedReader = new BufferedReader(new InputStreamReader(process.getInputStream(),"GBK"));
         String line = null;
         int index = -1;
         while ((line = bufferedReader.readLine()) != null) {
            System.out.println(line);
            index = line.toLowerCase().indexOf("物理地址");    //注意用ipconfig -all看一下字符，中英文是不一样的
            if (index != -1) {
               index = line.indexOf(":");
               if (index != -1) {
                  mac = line.substring(index + 1).trim();
               }
               break;
            }
         }
      } catch (IOException e) {
         e.printStackTrace();
      }finally {
         try {
            if (bufferedReader != null) {
               bufferedReader.close();
            }
         }catch (IOException e1) {
            e1.printStackTrace();
         }
         bufferedReader = null;
         process = null;
      }
      return mac;
   }
