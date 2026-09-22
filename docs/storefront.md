# VEXO Shopify Storefront

## Scope

The VEXO storefront is a Dawn-based Shopify Online Store 2.0 implementation.

The storefront work is maintained separately from the private backend automation system.

## Theme Architecture

The storefront uses Shopify-native primitives:

```text
Layout
  ↓
Templates
  ↓
Sections
  ↓
Snippets
  ↓
Theme assets
```

The implementation stays within the Online Store 2.0 theme model rather than replacing the storefront with a front-end framework.

## Engineering Areas

### Liquid and Sections
- Dawn-based section architecture
- Reusable snippets
- Product and collection presentation
- Cart and customer-facing behaviour
- Theme settings integrated with Shopify's native schema

### Commerce UX
Selected storefront capabilities include:

- sticky add-to-cart
- predictive search
- faceted filtering
- product recommendations
- cart upsells
- media zoom
- responsive product presentation

These are implemented using Shopify theme primitives and lightweight JavaScript where behaviour requires it.

### Performance
Performance work includes:

- responsive image handling
- lazy loading where appropriate
- reduced unnecessary asset work
- semantic markup
- careful client-side behaviour

The design target is not simply visual polish. The theme should preserve useful interaction while limiting avoidable browser work.

### Accessibility
Accessibility considerations include:

- semantic structure
- keyboard focus handling
- clear interactive states
- reduced-motion support
- accessible control labelling

### Automated Theme QA
Representative automated checks include:

- Shopify Theme Check
- JSON validation
- asset-reference checks
- targeted browser verification

The goal is to detect structural theme issues before visual or behavioural regressions reach the storefront.

## Storefront / Backend Boundary

The storefront should not contain private backend credentials or privileged server-side integration logic.

A safe division is:

```text
Shopify theme
   ↕
Shopify platform
   ↕
Private backend / integrations
```

The storefront presents commerce data and customer-facing interactions. Sensitive automation and external-system credentials remain on the server side.

## Public Boundary

This portfolio describes the storefront engineering without publishing private theme implementation details or operational configuration.

The private implementation remains available in the separate repository:

https://github.com/theprimelotus/web-vexo-ai
