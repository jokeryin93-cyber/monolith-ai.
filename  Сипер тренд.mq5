//+------------------------------------------------------------------+
//|                                    AI_MONOLITH_V26_MOBILE_READY  |
//|         STATUS: BOT #1 (GOLD H1) - СВЯЗЬ С ПРИЛОЖЕНИЕМ           |
//+------------------------------------------------------------------+
#property copyright "Joint Project 2026"
#property version   "26.95"
#property strict

#include <Trade\Trade.mqh>
#include <ChartObjects\ChartObjectsTxtControls.mqh>

//--- ДАННЫЕ ДЛЯ ТВОЕГО ПРИЛОЖЕНИЯ
string TG_Token = "8555330344:AAEP9EwBjmXouhpeGj0DdnY_HDAN5rzVxOk";
string TG_ChatID = "5223724165";

input double AI_Confidence  = 20.0;
input string Gemini_API_Key = "AIzaSyAu9VJEHUy18c6WaXhbVgZ06lIXdBix5D0";
input int    Max_Spread     = 150;

CTrade trade;
int hRSI, hMFI, hEMA; 
CChartObjectLabel gui_ai, gui_mode, gui_lot, gui_trend;

int OnInit() {
   hRSI = iRSI(_Symbol,_Period,14,PRICE_CLOSE); 
   hMFI = iMFI(_Symbol,_Period,14,VOLUME_TICK);
   hEMA = iMA(_Symbol,_Period,200,0,MODE_EMA,PRICE_CLOSE);
   
   gui_ai.Create(0,"AI_Status",0,10,30); gui_ai.Color(clrCyan);
   gui_trend.Create(0,"Trend",0,10,50);
   
   SendToApp("📱 [BOT #1: MONOLITH] Подключен к мобильному приложению!");
   return(INIT_SUCCEEDED);
}

void SendToApp(string msg) {
   string url = "https://api.telegram.org/bot"+TG_Token+"/sendMessage?chat_id="+TG_ChatID+"&text="+msg;
   char data[], res[]; string head;
   WebRequest("GET", url, NULL, 10000, data, res, head);
}

void OnTick() {
   static datetime last_bar = 0;
   if(last_bar != iTime(_Symbol,_Period,0)) {
      CheckSignals();
      last_bar = iTime(_Symbol,_Period,0);
   }
}

void CheckSignals() {
   double r[], m[], ema[];
   ArraySetAsSeries(r,true); ArraySetAsSeries(m,true); ArraySetAsSeries(ema,true);
   
   if(CopyBuffer(hRSI,0,0,1,r)>0 && CopyBuffer(hMFI,0,0,1,m)>0 && CopyBuffer(hEMA,0,0,1,ema)>0) {
      double str = (r[0]-50.0)+(m[0]-50.0);
      
      // Отправка зон в приложение
      if(r[0] > 75) SendToApp("⚠️ [MONOLITH] Зона продаж! Цена слишком высоко.");
      if(r[0] < 25) SendToApp("✅ [MONOLITH] Зона покупок! Отличное место для входа.");

      if(MathAbs(str) >= AI_Confidence) {
         string action = (str > 0) ? "BUY" : "SELL";
         string ai_res = AskGemini("Side: "+action+" RSI: "+DoubleToString(r[0],1));
         
         if(StringFind(ai_res, "YES") >= 0) {
            double pr = (action == "BUY") ? SymbolInfoDouble(_Symbol, SYMBOL_ASK) : SymbolInfoDouble(_Symbol, SYMBOL_BID);
            if(action == "BUY") trade.Buy(0.01,_Symbol,pr,0,0,"MONOLITH_APP");
            if(action == "SELL") trade.Sell(0.01,_Symbol,pr,0,0,"MONOLITH_APP");
            SendToApp("🎯 [MONOLITH] Открыл сделку " + action + " по сигналу ИИ!");
         }
      }
   }
}

string AskGemini(string text) {
   char data[], result[]; string headers;
   string url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + Gemini_API_Key;
   string request = "{\"contents\": [{\"parts\":[{\"text\": \"" + text + ". Answer only YES or NO.\"}]}]}";
   ArrayResize(data, StringToCharArray(request, data, 0, WHOLE_ARRAY, CP_UTF8) - 1);
   int res = WebRequest("POST", url, "Content-Type: application/json", 10000, data, result, headers);
   if(res == 200) return CharArrayToString(result, CP_UTF8);
   return "NO";
}