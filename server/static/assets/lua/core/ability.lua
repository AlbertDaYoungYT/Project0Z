-- static/assets/lua/core/ability.lua
local Ability = {}
Ability.__index = Ability

function Ability:new(o)
  o = o or {}
  -- Default properties for an ability
  o.name = o.name or "Unnamed Ability"
  o.description = o.description or ""
  o.cooldown = o.cooldown or 0
  o.cost = o.cost or 0 -- e.g., mana, energy
  o.target_type = o.target_type or "self" -- self, enemy, ally, area, none
  o.asset_type = "ability" -- For registration
  setmetatable(o, self)
  return o
end

-- Check if the ability can be used by the caster
-- caster_proxy: a proxy object representing the entity casting the ability
function Ability:can_use(caster_proxy)
  -- Placeholder: Implement checks like cooldown, resource cost, conditions
  -- log_info("Lua Ability:can_use for " .. self.name .. " by " .. (caster_proxy and caster_proxy.name or "unknown caster"))
  return true
end

-- Execute the ability's effect
-- caster_proxy: the entity casting the ability
-- target_proxy: the entity being targeted (optional, depends on target_type)
function Ability:on_use(caster_proxy, target_proxy)
  error("Ability:on_use must be implemented by specific ability: " .. self.name)
end

-- Called when the ability is learned or acquired
function Ability:_on_learn(caster_proxy)
  -- Optional: logic when an entity learns this ability
  -- log_info("Lua Ability:_on_learn for " .. self.name .. " by " .. (caster_proxy and caster_proxy.name or "unknown entity"))
end

function Ability:on_tick(infected_player_proxy)
  error("Ability:on_tick must be implemented by subclass")
end

return Ability