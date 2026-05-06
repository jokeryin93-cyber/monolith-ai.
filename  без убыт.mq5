//+------------------------------------------------------------------+
//|                                  SafeScalper_Pro_MOBILE_READY    |
//|         STATUS: BOT #2 (SCALPER)                                 |
//+------------------------------------------------------------------+
#property copyright "Joint Project 2026"
#property version   "1.05"
#property strict

#include <Trade\Trade.mqh>

//--- ДАННЫЕ ДЛЯ МОБИЛЬНОГО ПРИЛОЖЕНИЯ (ТВОИ КЛЮЧИ)
string TG_Token = "8555330344:AAEP9EwBjmXouhpeGj0DdnY_HDAN5rzVxOk";
string TG_ChatID = "5223724165";

input string Gemini_Key    = "AIzaSyAu9VJEHUy18c6WaXhbVgZ06lIXdBix5D0"; 
input double LotSize       = 0.01;      
input int    Max_Spread    = 35;        
input int    ATR_Period    = 14;        
input double Profit_Coeff  = 1.5;       
input double BE_Coeff      = 0.5;       

CTrade trade;

// Функция связи с твоим приложением
void SendToApp(string msg) {
   string url = "https://api.telegram.org/bot"+TG_Token+"/sendMessage?chat_id="+TG_ChatID+"&text="+msg;
   char data[], res[]; string head;
   WebRequest("GET", url, NULL, 10000, data, res, head);
}

void OnInit() {
   SendToApp("⚡️ [BOT #2: SCALPER] Активирован и готов к быстрой торговле!");
}

void OnTick()
{
   int spread = (int)SymbolInfoInteger(_Symbol, SYMBOL_SPREAD);
   if(spread > Max_Spread) return; 

   double atr[];
   int handle = iATR(_Symbol, _Period, ATR_Period);
   ArraySetAsSeries(atr, true);
   if(CopyBuffer(handle, 0, 0, 1, atr) < 1) return;
   double currentATR = atr[0];

   if(PositionsTotal() < 1)
   {
      string trend = AskGemini("Trend for " + _Symbol + " on " + EnumToString(_Period));
      
      if(StringFind(trend, "BUY") >= 0) {
         if(trade.Buy(LotSize, _Symbol, SymbolInfoDouble(_Symbol, SYMBOL_ASK), 0, 0, "SCALP_2")) {
            SendToApp("🚀 [SCALPER] BUY по " + _Symbol + "\nИИ подтвердил тренд, волатильность в норме.");
         }
      }
      else if(StringFind(trend, "SELL") >= 0) {
         if(trade.Sell(LotSize, _Symbol, SymbolInfoDouble(_Symbol, SYMBOL_BID), 0, 0, "SCALP_2")) {
            SendToApp("🚀 [SCALPER] SELL по " + _Symbol + "\nИИ подтвердил тренд, заходим по ATR.");
         }
      }
   }

   // Сопровождение сделки
   for(int i=PositionsTotal()-1; i>=0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(PositionSelectByTicket(ticket))
      {
         double entry = PositionGetDouble(POSITION_PRICE_OPEN);
         double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
         double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
         double diff = (PositionGetInteger(POSITION_TYPE)==POSITION_TYPE_BUY) ? (bid - entry) : (entry - ask);

         if(diff >= currentATR * BE_Coeff) 
         {
            double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
            double sl = PositionGetDouble(POSITION_SL);
            double newSL = (PositionGetInteger(POSITION_TYPE)==POSITION_TYPE_BUY) ? entry + (5*point) : entry - (5*point);
            
            if(sl == 0 || (PositionGetInteger(POSITION_TYPE)==POSITION_TYPE_BUY && newSL > sl) || (PositionGetInteger(POSITION_TYPE)==POSITION_TYPE_SELL && (newSL < sl || sl == 0))) 
            {
               if(trade.PositionModify(ticket, newSL, 0))
                  SendToApp("🛡️ [SCALPER] Сделка в безубытке. Риск 0!");
            }
         }
         
         if(diff >= currentATR * Profit_Coeff) 
         {
            trade.PositionClose(ticket);
            SendToApp("💰 [SCALPER] ПРОФИТ ВЗЯТ! Цель по ATR достигнута.");
         }
      }
   }
}

string AskGemini(string text) {
   char data[], result[]; string headers;
   string url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + Gemini_Key;
   string request = "{\"contents\": [{\"parts\":[{\"text\": \"Trader AI. " + text + ". Answer BUY or SELL only.\"}]}]}";
   ArrayResize(data, StringToCharArray(request, data, 0, WHOLE_ARRAY, CP_UTF8) - 1);
   int res = WebRequest("POST", url, "Content-Type: application/json", 10000, data, result, headers);
   if(res == 200) return CharArrayToString(result, CP_UTF8);
   return "NONE";
}