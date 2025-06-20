-- static/assets/lua/core/skill.lua
local Skill = {}
Skill.__index = Skill

Skill.TYPE = {
  PASSIVE = "passive",
  ACTIVE = "active"
}


function Skill:new(o)
  o = o or {}
  setmetatable(o, self)
  o.id = o.id or "unknown_skill"
  o.name = o.name or "Unknown Skill"
  o.description = o.description or "A mysterious skill."
  o.type = o.type or Skill.TYPE.PASSIVE
  o.cooldown = o.cooldown or 0
  o.current_cooldown = 0
  o.cost = o.cost or {} -- e.g., { mana = 10 }
  o.effects = o.effects or {} -- List of effect functions
  return o
end

function Skill:can_use(user)
  if self.current_cooldown > 0 then
    return false, "Skill is on cooldown."
  end
  for resource, amount in pairs(self.cost) do
    if (user.resources and user.resources[resource] or 0) < amount then
      return false, "Not enough " .. resource .. "."
    end
  end
  return true
end

function Skill:use(user, target)
  if not self:can_use(user) then
    return false, "Cannot use skill."
  end

  -- Deduct cost
  for resource, amount in pairs(self.cost) do
    if user.resources then
      user.resources[resource] = (user.resources[resource] or 0) - amount
    end
  end

  -- Apply effects
  for _, effect in ipairs(self.effects) do
    effect(user, target, self)
  end

  -- Start cooldown
  self.current_cooldown = self.cooldown

  return true
end

function Skill:update(dt)
  if self.current_cooldown > 0 then
    self.current_cooldown = math.max(0, self.current_cooldown - dt)
  end
end

return Skill
