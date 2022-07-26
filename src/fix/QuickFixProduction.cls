Class fix.QuickFixProduction Extends Ens.Production
{

XData ProductionDefinition
{
<Production Name="fix.QuickFixProduction" TestingEnabled="true" LogGeneralTraceEvents="false">
  <Description></Description>
  <ActorPoolSize>2</ActorPoolSize>
  <Item Name="Python.FixOrder" Category="" ClassName="Python.FixOrderOperation" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="%settings">BeginString=FIX.4.3
SenderCompID=CLIENTORDER
TargetCompID=SERVER
HeartBtInt=30
SocketConnectPort=3000
SocketConnectHost=acceptor
DataDictionary=/irisdev/app/src/fix/spec/FIX43.xml
FileStorePath=/irisdev/app/src/fix/Sessions/
ConnectionType=initiator
FileLogPath=/irisdev/app/src/fix/Logs/
StartTime=00:00:00
EndTime=00:00:00
ReconnectInterval=2
LogoutTimeout=5
LogonTimeout=5
ResetOnLogon=Y
ResetOnLogout=Y
ResetOnDisconnect=Y
SendRedundantResendRequests=Y
SocketNodelay=N
ValidateUserDefinedFields=N
ValidateFieldsOutOfOrder=N</Setting>
    <Setting Target="Adapter" Name="KeepaliveInterval">1</Setting>
  </Item>
  <Item Name="Python.FixQuote" Category="" ClassName="Python.FixQuoteOperation" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="%settings">BeginString=FIX.4.3
SenderCompID=CLIENTQUOTE
TargetCompID=SERVER
HeartBtInt=30
SocketConnectPort=3000
SocketConnectHost=acceptor
DataDictionary=/irisdev/app/src/fix/spec/FIX43.xml
FileStorePath=/irisdev/app/src/fix/Sessions/
ConnectionType=initiator
FileLogPath=/irisdev/app/src/fix/Logs/
StartTime=00:00:00
EndTime=00:00:00
ReconnectInterval=10
LogoutTimeout=5
LogonTimeout=5
ResetOnLogon=Y
ResetOnLogout=Y
ResetOnDisconnect=Y
SendRedundantResendRequests=Y
SocketNodelay=N
ValidateUserDefinedFields=N
ValidateFieldsOutOfOrder=N</Setting>
    <Setting Target="Adapter" Name="KeepaliveInterval">1</Setting>
    <Setting Target="Adapter" Name="%settings">subscribe=True
MarketDepth=0
MDUpdateType=0
SecurityType=FOR
md_types=0;1
symbols=EUR/USD;USD/CZK
products=4;4</Setting>
  </Item>
  <Item Name="Python.FixBusinessProcess" Category="" ClassName="Python.FixBusinessProcess" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
  </Item>
</Production>
}

}
