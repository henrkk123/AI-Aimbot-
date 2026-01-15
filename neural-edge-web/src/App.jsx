import React, { useState, useEffect } from "react"
import { motion } from "framer-motion"
import {
    Zap,
    Target,
    Cpu,
    Github,
    Crosshair,
    ArrowUpRight,
    Terminal,
    Activity,
    Maximize2
} from "lucide-react"

const GlitchText = ({ text }) => (
    <div className="relative inline-block group">
        <span className="relative z-10">{text}</span>
        <span className="absolute top-0 left-0 -z-10 text-accent opacity-0 group-hover:opacity-100 group-hover:translate-x-1 transition-all duration-75">{text}</span>
        <span className="absolute top-0 left-0 -z-20 text-red-500 opacity-0 group-hover:opacity-100 group-hover:-translate-x-1 transition-all duration-75">{text}</span>
    </div>
)

const Nav = () => (
    <nav className="fixed top-0 left-0 w-full z-[100] px-6 py-8 flex justify-between items-start pointer-events-none">
        <div className="pointer-events-auto">
            <div className="text-2xl font-black tracking-tighter uppercase italic bg-white text-black px-2 py-1 flex items-center gap-2">
                <Zap size={20} fill="currentColor" /> Axion.Engine
            </div>
            <div className="text-[10px] mono mt-2 text-white/40 font-bold tracking-[0.3em] uppercase">Status: Undetected_Core_v0.5.5</div>
        </div>

        <div className="pointer-events-auto flex flex-col items-end gap-2 mono text-[11px] uppercase tracking-tighter">
            <a href="#" className="hover:text-accent transition-colors bg-white/5 px-3 py-1 border border-white/10 hover:border-accent">// Main_Terminal</a>
            <a href="#" className="hover:text-accent transition-colors bg-white/5 px-3 py-1 border border-white/10 hover:border-accent">// Documentation</a>
            <a href="#" className="hover:text-black hover:bg-white transition-all bg-accent text-black px-3 py-1 font-bold">Launch_Control</a>
        </div>
    </nav>
)

const Hero = () => (
    <section className="relative min-h-screen pt-40 pb-20 px-6">
        <div className="max-w-[1400px] mx-auto">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-end">

                <div className="lg:col-span-8">
                    <motion.div
                        initial={{ opacity: 0, x: -50 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.8 }}
                    >
                        <h1 className="text-[12vw] leading-[0.8] font-black uppercase tracking-tighter italic">
                            UNFAIR <br />
                            <span className="text-accent underline decoration-8 underline-offset-[10px]">ADVANTAGE</span>
                        </h1>

                        <p className="mt-12 text-2xl md:text-4xl text-white/60 font-medium max-w-3xl leading-tight uppercase tracking-tight">
                            We took the math of <span className="text-white italic underline">perfection</span> and turned it into a weapon. Built for those who refuse to pay $100/mo for a private cheat.
                        </p>
                    </motion.div>
                </div>

                <div className="lg:col-span-4 flex flex-col gap-6 mono">
                    <div className="p-6 border-l-4 border-accent bg-white/5 space-y-4">
                        <div className="flex justify-between items-center text-[10px] text-white/50 border-b border-white/10 pb-2">
                            <span>SYSTEM_STATS</span>
                            <Activity size={12} className="text-accent" />
                        </div>
                        <div className="text-sm font-bold flex justify-between">
                            <span>LATENCY:</span>
                            <span className="text-accent">0.24ms</span>
                        </div>
                        <div className="text-sm font-bold flex justify-between">
                            <span>UPTIME:</span>
                            <span>99.9%</span>
                        </div>
                        <div className="text-sm font-bold flex justify-between">
                            <span>VERSION:</span>
                            <span className="bg-white text-black px-1 leading-none uppercase">v0.5.5_Blackwell</span>
                        </div>
                    </div>

                    <button className="w-full bg-white text-black py-4 font-black text-xl uppercase italic hover:bg-accent transition-all flex items-center justify-between px-6 group overflow-hidden relative">
                        <span className="relative z-10 transition-transform group-hover:translate-x-2">Download_Axion_Client</span>
                        <Maximize2 className="relative z-10 group-hover:scale-125 transition-transform" />
                        <div className="absolute top-0 -left-full w-full h-full bg-accent transition-all group-hover:left-0 -z-0 opacity-20" />
                    </button>
                </div>

            </div>
        </div>
    </section>
)

const FeatureRow = ({ num, title, desc, tag }) => (
    <div className="grid grid-cols-1 md:grid-cols-12 gap-6 py-12 border-b border-white/10 group cursor-default">
        <div className="md:col-span-1 mono text-white/20 text-4xl font-black">{num}</div>
        <div className="md:col-span-4">
            <h3 className="text-4xl font-black uppercase italic group-hover:text-accent transition-colors"><GlitchText text={title} /></h3>
            <div className="mt-2 text-[10px] mono bg-white/10 w-fit px-2 py-0.5 text-accent">{tag}</div>
        </div>
        <div className="md:col-span-5 text-lg text-white/50 leading-relaxed uppercase tracking-tight">
            {desc}
        </div>
        <div className="md:col-span-2 flex items-start justify-end">
            <ArrowUpRight className="text-white/20 group-hover:text-accent transition-colors" size={40} />
        </div>
    </div>
)

const TechShowcase = () => (
    <section className="py-40 px-6">
        <div className="max-w-[1400px] mx-auto">
            <div className="flex items-end justify-between mb-20">
                <h2 className="text-[8vw] font-black leading-none uppercase italic tracking-tighter">SPECS_</h2>
                <div className="mono text-[10px] text-white/30 text-right max-w-[200px]">THE RAW ARCHITECTURE OF THE DOMINATION SUITE</div>
            </div>

            <FeatureRow
                num="01"
                title="Axic_Lock"
                tag="SM_120_OPTIMIZED"
                desc="Vector-based prediction that calculates target trajectory before it even happens. Mathematically superior tracking."
            />
            <FeatureRow
                num="02"
                title="Ghost_Mode"
                tag="UNDETECTABLE_INP"
                desc="Windows API layering that makes our input indistinguishable from real human movement. Zero footprint."
            />
            <FeatureRow
                num="03"
                title="Smart_Mask"
                tag="3RD_PERSON_FIX"
                desc="Dynamic character exclusion. The engine ignores your own model and locks onto the only thing that matters: The Win."
            />
            <FeatureRow
                num="04"
                title="Blackwell_FW"
                tag="NVIDIA_RTX_50"
                desc="Custom CUDA kernels written specifically for the SM_120 architecture. Maximum frames, minimum latency."
            />

        </div>
    </section>
)

const Manifesto = () => (
    <section className="py-40 bg-white text-black overflow-hidden relative">
        <div className="absolute top-0 right-0 p-10 mono opacity-10 text-[20vw] font-black pointer-events-none tracking-tighter leading-none italic">AXION</div>
        <div className="max-w-[1400px] mx-auto px-6 relative z-10">
            <h2 className="text-[10vw] font-black leading-[0.8] uppercase italic mb-20 tracking-tighter">
                F*CK <br />PAY-TO-WIN.
            </h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-20 items-start">
                <div className="space-y-8">
                    <p className="text-4xl font-bold uppercase italic leading-none">
                        We are tired of "Private Cheats" costing $200 a month. Performance shouldn't be a subscription service.
                    </p>
                    <div className="w-20 h-2 bg-black" />
                    <p className="text-xl font-medium uppercase mono">
                        Axion Engine is our middle finger to the industry. High-end code. Zero dollars. Everything open source. Forever.
                    </p>
                </div>
                <div className="border-t-4 border-black pt-10">
                    <Terminal size={40} className="mb-6" />
                    <div className="mono text-xs space-y-2 opacity-60">
                        <p>root@axion:~$ ./deploy_freedom.sh</p>
                        <p>Environment: Windows 10/11 x64</p>
                        <p>Target: Competitive Meta</p>
                        <p>Status: Unstoppable_Force</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
)

const Footer = () => (
    <footer className="py-20 px-6 border-t border-white/5">
        <div className="max-w-[1400px] mx-auto flex flex-col md:flex-row justify-between items-center gap-10">
            <div className="flex items-center gap-4 bg-white text-black px-4 py-2 font-black italic uppercase tracking-tighter">
                <Zap size={20} fill="currentColor" /> Axion_Engine_Core
            </div>
            <div className="mono text-[10px] text-white/20 tracking-[0.5em] uppercase italic">REVOLUTION_STAY_ELITE_2026</div>
            <div className="flex gap-10 mono text-[11px] font-bold uppercase tracking-tight">
                <a href="#" className="hover:text-accent">X.com</a>
                <a href="#" className="hover:text-accent">Discord</a>
                <a href="#" className="hover:text-accent">Github</a>
            </div>
        </div>
    </footer>
)

export default function App() {
    return (
        <div className="bg-[#050505] min-h-screen text-white relative">
            <div className="scanlines z-[999]" />
            <Nav />
            <Hero />
            <TechShowcase />
            <Manifesto />
            <Footer />
        </div>
    )
}
