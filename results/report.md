# Feasible customer visits before a convincing itinerary

On 30 original two-day scenarios with 7 sites each, subset/time-window dynamic programming selects 152 visits worth 1200 fictional priority points; highest-priority-first greedy selects 119 worth 983. The exact method has strictly greater utility in 26 scenarios. An independent replay verifies every returned plan.

The usual failure is spending a day on one attractive remote appointment while losing several compatible visits. My approach computes feasible daily subsets with earliest-finish dominance, then combines disjoint subsets across days. Hard constraints are verified separately from priority points.

The objective is chosen, not discovered: site values and visit costs are fictional assumptions, not revenue. Exactness applies only to this static bounded formulation; no time-varying traffic, meetings booked by others, or uncertain customer availability is modeled. The next step is robust planning under travel-time ranges, not a claim that the same plan should be scheduled in a real calendar.
