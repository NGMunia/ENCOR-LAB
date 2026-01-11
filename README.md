# ENCOR Enterprise Network Lab

**A full-scale enterprise and service-provider lab showcasing advanced routing, overlays, security, automation, QoS, and network assurance.**  
Designed to reflect enterprise network architectures aligned with **CCNP Enterprise (ENCOR)** objectives.

![BGP](https://img.shields.io/badge/BGP-Advanced-blue)
![DMVPN](https://img.shields.io/badge/DMVPN-Phase%202-green)
![Security](https://img.shields.io/badge/Security-Enterprise-red)
![Automation](https://img.shields.io/badge/Automation-Python%20%7C%20FastAPI-orange)
![CCNP](https://img.shields.io/badge/CCNP-ENCOR-success)

---

## Quick Overview

- **Routing:** Multi-AS BGP, traffic engineering, summarization
- **Overlays:** DMVPN, LISP, IPsec VTI
- **Security:** Zone-Based Firewall, CoPP, segmentation, NAT
- **Automation:** Python, FastAPI, Netmiko, Jinja2
- **Monitoring:** SNMP, NetFlow
- **Level:** CCNP Enterprise (ENCOR)

---

## Project Objectives

- Design and implement multi-AS enterprise routing
- Apply BGP traffic engineering techniques
- Deploy scalable WAN overlay technologies
- Secure network infrastructure and control planes
- Automate repetitive network operations
- Monitor and analyze network performance and traffic flows

---

## Network Architecture

The lab simulates a hybrid **enterprise** environment with multiple autonomous systems, enterprise customers, and secure overlays.



---

## Routing & BGP Design

### AS 123 – Enterprise Edge

- Non-transit autonomous system
- Outbound traffic via **R1** using **VRRPv3**
- VRRP object tracking integrated with **IP SLA**
- Inbound traffic influenced via **AS-path prepending** toward **R2**
- Provides resiliency, redundancy, and deterministic traffic flow

### Private VLANs

Implemented on the access switch to isolate customer traffic:

- **Community VLAN 100** – Company-X
- **Isolated VLAN 101**

Prevents lateral communication while maintaining shared infrastructure.

---

### BGP Autonomous Systems Overview

| AS Number | Function |
|---------|---------|
| AS 123 | Enterprise non-transit AS with traffic engineering |
| AS 130 | Removes private AS, advertises `17.17.17.0/24`, sends default route |
| AS 140 | Advertises summary prefix `140.140.140.0/24` |
| AS 150 | Advertises summary prefix `150.150.150.0/24` |
| AS 65530 | Upstream provider advertising summarized routes |

---

## Overlay Technologies

### Company-X – DMVPN

- **DMVPN Phase 2**
- HQ acts as hub, Branch and R5 as spokes
- **OSPF** used as the overlay routing protocol
- Tunnel interface configured in **Area 0**
- Internal networks:
  - HQ – Area 10
  - Branch – Area 20
  - R5 – Area 50

Demonstrates scalable and resilient enterprise WAN design.

---

### Company-A – LISP

- **LISP** used to advertise prefixes behind R16 and R26
- Runs on top of **mGRE** for privacy
- **R6** acts as Map Server and Map Resolver
- Separates endpoint identity from location for scalability

---

### Cust-A – IPsec VTI

- **IPsec VTI** tunnel between R7 and R8
- Supports multicast traffic over VPN
- **PIM Sparse Mode** with a static Rendezvous Point (RP)

---

## Automation & Programmability

### Company-X Automation

- Automated repetitive router configurations (e.g. SNMP)
- Developed custom **REST APIs** using **FastAPI**
- Integrated **Netmiko** for network device interaction
- Used **Jinja2 templates** for reusable and scalable configuration generation

Demonstrates API-driven automation and infrastructure-as-code principles.

---

## Quality of Service (QoS)

### Company-X LAN Router

- Social media traffic policed to **250 kbps**
- Scavenger traffic (torrent) dropped
- Traffic destined to **R5** marked as critical
- Critical traffic allocated **30% CBWFQ bandwidth** of CIR

Implements enterprise-grade traffic classification and prioritization.

---

## Network Address Translation (NAT)

- Router labeled **HTTP** emulates a web server
- Port forwarding configured on **R4**
- HTTP service accessible via:

```text
http://44.67.28.4/

```

---

##  Network Assurance

### Company-X
 - SNMP is configured on all Company-X routers to be monitored on the Server
 - NetFlow is configured on LAN, R5 and Branch-1 routers to monitor traffic type traversing  from the LAN network

---
## Security:

Company-X firewall
  - Zone based firewall is configured to separate LAN and Internet links
  - Control-plane policing has been configured on HQ, R5 and Branch routers


## Images used:

  - Routers:  i86bi-linux-l3-adventerprisek9-ms.155-2.T.bin
  - Switches: i86bi_linux_l2-adventerprise-ms.high_iron_20170202.bin
  - Server:   Win2k16_14393.0.161119-1705.RS1_REFRESH_SERVER_EVAL_X64FRE_EN-US.ISO
  - Ubuntu:   Ubuntu Desktop VM
  - PCs:      Webterm docker


