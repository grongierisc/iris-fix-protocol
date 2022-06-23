Class FIX.Production Extends Ens.Production
{

XData ProductionDefinition
{
<Production Name="FIX.Production" TestingEnabled="true" LogGeneralTraceEvents="false">
  <Description></Description>
  <ActorPoolSize>2</ActorPoolSize>
  <Item Name="FIX.bo.FixBusinessOperation" Category="" ClassName="FIX.bo.FixBusinessOperation" PoolSize="1" Enabled="true" Foreground="false" Comment="" LogTraceEvents="false" Schedule="">
  </Item>
</Production>
}

}
