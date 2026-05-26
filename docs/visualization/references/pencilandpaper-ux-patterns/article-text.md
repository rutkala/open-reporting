# Dashboard Design UX Patterns

January 2, 2025 — Fanny Vassilatos and Ceara Crawshaw

---

Whether it's for analytical, operational or strategic purposes, being able to interpret the right information at a glance is pivotal for teams and departments of all sizes. When designing a data dashboard for your own enterprise product, your team needs to be very intentional about what data points get showcased. Make no mistake, data dashboard UX is tricky.

## Why does dashboard design matter?

A product's dashboards serve a critical purpose in exposing key data and actionable insights – effectively exposing what's under the hood in a way that's useful. Dashboards serve to extend the possibilities of what can be achieved through our use of software.

*Dashboards* – the term is often synonymous with the concept of a homepage in an application or even any experience where there is a sprinkle of data vis.

## Why are dashboards relevant to enterprise software?

In data-heavy platforms, a common pain point is navigating multiple data sources and disjointed systems. Dashboards can unite those systems together and provide a global overview.

- They amalgamate multiple data sources to give us a clearer picture of what's going on
- They visualize data so we can sense the dynamics between different things
- They are typically quite efficient representations of systems which helps to manage things

## Dashboards are challenging

Designing excellent dashboards is a very complex process which is super difficult to get right, even when you're using all the best UX practices.

**Data-wise** – It's difficult to understand the data model and the state of the data in its entirety — this is especially true when data varies from customer to customer.

**User testing** – conducting user testing with Figma prototypes is difficult, because the data we fudge doesn't really reflect the participants dataset.

**Technical challenges** – Using out-of-the-box libraries is very typical for dashboards, which inevitably brings unexpected constraints.

**Performance** – sometimes the experience is undermined by performance drama, where massive datasets need to do a ton of computing on the fly.

## Things to consider for your dashboard UX design

**Is the data clean enough?**

The very first thing you get to do is a data architecture analysis. What data do you even have? Is the data maintainable? Is the metadata consistent and scalable?

- Is the data tracked over time?
- How much historical data do we have? (years, months etc)
- Can we calculate if/when statements to create insights?

**Map out user context**

As much as it would be nice to design a dashboard for each persona, that wouldn't be very efficient. Find the overlaps and divergences. Aim to keep it global at first (default state) + allow for granularity with interactions.

**Determine dashboard design goals**

What are users expecting to do with that screen? What questions do they need the dashboard to answer?

- What needs their attention?
- What do they need to report on?
- What deserves a spot on the dashboard?
- What are the most global metrics that deserve higher visibility?
- What needs to be visualized?

**Prioritize warnings and actionable items**

Surface the key stuff they can take action on, and any warnings they should quickly be made aware of.

**Find out what is taking the most time for users to compile**

Try to prioritize which charts will actually make it to the dashboard. What are users currently doing to obtain this information? Which things do they do every day? Versus once a month or once a quarter?

## Types of dashboard experiences and use cases

**Reporting** — Comprehensive or overview content, often serves to amalgamate data all together. Often you see an export function and/or share functionality. The point is to tell a story with data. Ex. quarterly earnings data.

**Monitoring** — This functions to alert and warn users. Data may be live and ticking away in realtime. Ex. monitoring a fleet of smart devices or web uptime/downtime.

**Exploring and discovery** — This functions to give users a means to discover data and infer insights. Ex. Open data experiences like Our World in Data.

**Functional and integrated** — This functions to guide users towards where they need to focus. Ex. a project management tool showing "at risk" tasks in a queue.

**Product home page** — This functions as a contextual index. It's more about giving an overview as well as serving as navigation. Ex. a SaaS application for marketing which shows main sections like leads and sales with totals and deltas.

## Anatomy of dashboard UX

### Navigation

Without getting into the ins and outs of navigation: follow navigation patterns and best practices so that when people reach the dashboard experience they are at an advantage.

### Getting Oriented

Upon navigating to the page itself, the user does the mental lift of figuring out: what the page is for, what it's showing me, what it's meant to do.

Recommendations:
- A clear page title — so people can immediately know what the point of the page is overall
- A clear description of the page — so people can understand what they can do there
- Charts and graphs are conceptually grouped together — so that people can understand what should be considered together and separately
- Jargon is explained via tooltips and other forms of descriptions

Don't forget to include any **loading feedback** and **empty states** that might apply to the page.

### Filtering and parsing the data

Prioritize the filters presented by default to be super useful. Don't forget loading UX considerations.

### Drilling into information

Drilling further into the information to reveal more detail is an important part of the experience.

**Drawer pattern** — allows a lot of flexible space to present information without having to exit the context you're currently in.

**Details page** — allows you to house a whole bunch of details in an entire view.

### Executing actions

- Interaction feedback – use success and error feedback as needed
- Multi-select – make sure that multiselect interactions are obvious and have appropriate affordances
- Prioritize actions – make the most important the most noticeable and the least important, the least noticeable
- For multiple actions, they can be housed in a dropdown button

## Layout UI patterns for dashboards

### Intuitive page layout

For left-to-right (LTR) language speakers, consider the F and Z patterns. The F shape suggests that the eye will naturally get drawn to the top-left corner at first and then scan horizontally, before zig-zagging down the page.

Since the top left area gets more attention, that's where you want to showcase the most global numbers, or the most relevant data.

Structure your charts and graphs into related sections going top-down. Starting with the most important at the top, following with a global overview in the middle, and wrapping up with a more detailed breakdown at the bottom.

### Consistent card layout

Card layouts are very common for data dashboards. Consistency is key — if users can quickly find the title on the top left of each module, or the legend always at the bottom center, that reduces visual noise when they scan the page.

## Chart UX patterns

### Use of colour

Smart use of colour is a very elegant way to provide additional meaning to the data.

Some charts benefit from a secondary palette — different shades of the same colour to express levels of intensity. Higher values could indicate larger quantities or densities.

Blues and oranges provide the same levels of vibrancy and contrast as greens and reds, without the UI feeling like a trading terminal.

### Lines, fills and textures

It's considered best practice not to rely on colour alone. Look for ways to add hashes or texture in fills and legends. A line chart with a bunch of solid lines in different colours can quickly become hard to interpret — add a variety of styles of dotted lines.

### Deltas

Deltas showcase differences (diffs). When relevant, make sure charts bring forward consistent deltas. They can be relative (% change since same day last month) or absolute (absolute difference compared to global average). Deltas should catch the eye and be quick and easy to make sense of.

### Responsiveness

When adapting your dashboard UX design for mobile, the first question is whether all the information is relevant for your users' "on-the-go" scenarios. Chances are they don't need it all.

### Data labels on charts

When dealing with large timescales or datasets, negotiating space might become a bit tricky. Angled labels typically work well, but there's always a limit. Don't hesitate to hide some labels altogether and leverage tooltips in denser views.

### Typography & hierarchy

Big bold numbers in a stylish display font can really help the functionality of your dashboard. They catch the eye. If you've done your research and identified the right numbers to accentuate this way, it demonstrates confidence and decisiveness.

## Interactive graphs and charts

### Tooltips & hover states

Hover states are the perfect way to hide that secondary layer of detail while avoiding visual noise. Since the goal of the dashboard is to provide an at-a-glance snapshot, the visual of bars or lines should be enough for users to sense the trends. Revealing additional detail upon hover is a great use of progressive disclosure.

### Toggling variables

Turning on and off certain variables can be relevant for some charts. Let's say the default view of a line chart presents 7 different lines — it might be useful for the user to hide some so they can focus on comparing a smaller selection. This can be implemented by making legend items into a checkbox list.

### Filters within dashboards

You can offer a full-page filter sidebar (or horizontal bar) where the filter selection affects the whole page. Another option is smaller filter options inside each module or section.

### Custom personalized dashboard patterns

Options: allow users to move modules around by drag-and-dropping; let them hide and show sections; integrate a custom "build your own dashboard" flow in onboarding UX.

## Common dashboard UX problems

### Density disjoint problem

The data eyeball attack — it's like a wall of text, but make it data. The density of the data makes users run for the hills. If there's some room to integrate a visual break, extra whitespace, or just a little bit less shown by default, try it out.

### Data seems random and unfocused

The attitude "we have it, so why not show it?" shows serious diminishing returns — more and more charts serve to destabilize users, as they assume if it's present, then it must be important. The hard work of information architecture is what actually makes a data dashboard experience great.

### Comparisons and baselines are lacking

Cognitive landmarks (like average or target numbers) can really help gauge where we are and what we're looking at. Without comparison, data feels like just a bunch of numbers.

### Technical jargon and lack of information

Acronyms are used to shorten things, but explanations in the form of tooltips, legends or other mechanisms are missed. Apply the lens of someone with zero context.

### Colour-coding mishaps

Only using colour to indicate the status of something can leave colour-blind users in the dark. Colour can also be overused easily in data dashboards — a rainbow salad with nothing sticking out as important.
