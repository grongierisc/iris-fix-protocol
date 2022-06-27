Class INFORMATION.QuickFixProduction Extends Ens.Production
{

XData ProductionDefinition
{
<Production Name="INFORMATION.QuickFixProduction" TestingEnabled="true" LogGeneralTraceEvents="false">
  <Description></Description>
  <ActorPoolSize>2</ActorPoolSize>
  <Item Name="Python.FixBusinessOperation" Category="" ClassName="Python.FixBusinessOperation" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="%settings"></Setting>
  </Item>
  <Item Name="Python.Application" Category="" ClassName="Python.Application" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
  </Item>
  <Item Name="Python.FixBusinessOperation2" Category="" ClassName="Python.FixBusinessOperation" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
    <Setting Target="Host" Name="%settings">DataDictionary=/src
UseDataDictionary=N
BeginString=FIX.4.0</Setting>
  </Item>
</Production>
}

}
