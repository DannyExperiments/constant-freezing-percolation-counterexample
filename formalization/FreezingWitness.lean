import Std

namespace FreezingWitness

/- Bit masks for the endpoint sets of 01,02,03,12,13,23, in that order. -/
def edges : List (Nat × Nat) := [(1,3),(2,5),(4,9),(8,6),(16,10),(32,12)]

def liveEdges (opened frozen : Nat) : List (Nat × Nat) :=
  edges.filter fun (bit, ends) => opened &&& bit == 0 && frozen &&& ends == 0

/-- Compute the connected components on warm vertices by merging singleton
blocks along every open edge whose endpoints are still warm. -/
def warmBlocks (opened frozen : Nat) : List Nat :=
  let singles := [1,2,4,8].filter (fun v => v &&& frozen == 0)
  edges.foldl (fun blocks (bit,ends) =>
    if opened &&& bit == 0 || frozen &&& ends != 0 then blocks
    else
      let (touch,rest) := blocks.partition fun block => block &&& ends != 0
      touch.foldl (· ||| ·) 0 :: rest) singles

/-- Backward first-jump recursion for missing the edge class mask.
Opening rates are 1000, freezing rates 1. One step either opens an edge
or freezes at least one vertex. Ten transitions suffice for K4. The
result is none if any contributing branch exhausts the traversal bound. -/
def miss (mask : Nat) : Nat → Nat → Nat → Option Rat
  | fuel, opened, frozen =>
    if opened &&& mask != 0 then some 0 else
    let live := liveEdges opened frozen
    if live.isEmpty then some 1 else
    match fuel with
    | 0 => none
    | fuel+1 => do
      let blocks := warmBlocks opened frozen
      let openWeight ← live.foldlM (fun acc e => return acc + (← miss mask fuel (opened ||| e.1) frozen)) 0
      let freezeWeight ← blocks.foldlM (fun acc b => return acc + (← miss mask fuel opened (frozen ||| b))) 0
      return (1000 * openWeight + freezeWeight) / (1000 * live.length + blocks.length : Nat)

/-- Each mask corresponds to exactly the edge class in the paper. -/
theorem classes :
    (edges.filter (fun e => e.1 &&& 33 != 0)).map Prod.snd = [3,12] ∧
    (edges.filter (fun e => e.1 &&& 30 != 0)).map Prod.snd = [5,9,6,10] := by decide

theorem empty_probability : miss 63 10 0 0 = some (1/752753001) := by decide +kernel
theorem matching_miss : miss 33 10 0 0 = some (1851450375416038843001/5036444772027457882094001) := by decide +kernel
theorem complement_miss : miss 30 10 0 0 = some (757610283767003/7543348363821273003) := by decide +kernel

theorem negative_covariance :
    (miss 63 10 0 0).getD 0 - (miss 33 10 0 0).getD 0 * (miss 30 10 0 0).getD 0 < 0 := by
  rw [empty_probability, matching_miss, complement_miss]
  decide +kernel

end FreezingWitness
#print axioms FreezingWitness.negative_covariance
