-- static/assets/lua/core/entity.lua
local Entity = {}
Entity.__index = Entity

function Entity:new(o)
  o = o or {}
  o.name = o.name or "Unknown Entity"
  o.entity_type = o.entity_type or "generic" -- e.g., player, npc, monster
  o.level = o.level or 1
  o.asset_type = "entity" -- For registration
  
  o.stats = o.stats or {
    health = o.health or 100,
    max_health = o.max_health or 100,
    mana = o.mana or 50,       -- Example resource
    max_mana = o.max_mana or 50,
    strength = o.strength or 10,
    agility = o.agility or 10,
    intellect = o.intellect or 10
    -- etc. Can be populated by core.stat instances
  }
  
  o.inventory = o.inventory or {} -- Could be a more complex inventory object/table
  o.abilities = o.abilities or {} -- Table of learned ability instances or keys
  o.active_effects = o.active_effects or {} -- Effects currently affecting the entity

  setmetatable(o, self)
  return o
end

-- Apply damage to the entity
-- amount: number, the amount of damage
-- damage_type: string, e.g., "physical", "fire"
-- source_entity_proxy: (optional) proxy of the entity that dealt the damage
function Entity:take_damage(amount, damage_type, source_entity_proxy)
  -- log_info("Lua Entity " .. self.name .. " taking " .. amount .. " damage of type " .. (damage_type or "generic"))
  self.stats.health = math.max(0, self.stats.health - amount)
  if self.stats.health == 0 then
    self:_on_death(source_entity_proxy)
  end
  -- Potentially trigger events or effects via Python bridge
end

-- Heal the entity
-- amount: number, the amount to heal
-- source_entity_proxy: (optional) proxy of the entity that healed
function Entity:heal(amount, source_entity_proxy)
  -- log_info("Lua Entity " .. self.name .. " healing " .. amount)
  self.stats.health = math.min(self.stats.max_health, self.stats.health + amount)
  -- Potentially trigger events or effects
end

-- Add experience points to the entity
-- amount: number, XP amount
function Entity:add_xp(amount)
  -- log_info("Lua Entity " .. self.name .. " gained " .. amount .. " XP")
  -- Placeholder for XP and level-up logic, potentially calling _on_level_up
end

-- Called when the entity dies
-- killer_proxy: (optional) proxy of the entity that caused the death
function Entity:_on_death(killer_proxy)
  log_info("Lua Entity: " .. self.name .. " has died. Killed by: " .. (killer_proxy and killer_proxy.name or "unknown source"))
  -- Placeholder for death logic (e.g., drop loot, respawn timer)
end

-- Called when the entity levels up
function Entity:_on_level_up()
  self.level = self.level + 1
  log_info("Lua Entity: " .. self.name .. " has reached level " .. self.level .. "!")
  -- Placeholder for stat increases, learning new abilities, etc.
end

-- Add an effect to the entity (e.g., from core.effect)
-- effect_instance: an instance of an effect (Lua table)
function Entity:add_effect(effect_instance, caster_proxy)
    table.insert(self.active_effects, effect_instance)
    if effect_instance._on_applied then
        effect_instance:_on_applied(self, caster_proxy) -- Pass entity self (Lua table) and optional caster
    end
    -- log_info("Lua Entity: Effect '" .. (effect_instance.name or "Unnamed Effect") .. "' applied to " .. self.name)
end

-- Update active effects (e.g., called every game tick from Python)
-- dt: delta time
function Entity:update_effects(dt)
    for i = #self.active_effects, 1, -1 do
        local effect = self.active_effects[i]
        if effect._on_tick then effect:_on_tick(self, dt) end -- Pass entity self (Lua table)
        if effect._while_applied then effect:_while_applied(self, dt) end
        -- Add logic for effect duration and removal if expired, then call effect:_on_removed(self)
    end
end

return Entity