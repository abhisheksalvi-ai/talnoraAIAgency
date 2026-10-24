/**
 * Frontend component tests using Vitest
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';

import { KPICard, KPIGrid } from '@/components/kpi-cards';
import { AgentControlCenter, AgentStatusBadge } from '@/components/agent-control-center';
import { CandidatePipelineFunnel } from '@/components/pipeline-funnel';
import { CopilotChatPanel } from '@/components/copilot-panel';
import { AutonomyModeSelector } from '@/components/autonomy-selector';


describe('KPI Cards', () => {
  it('renders KPI card with value and title', () => {
    render(
      <KPICard 
        title="TEST METRIC" 
        value={42}
        subtext="Test subtitle"
      />
    );
    
    expect(screen.getByText('TEST METRIC')).toBeInTheDocument();
    expect(screen.getByText('42')).toBeInTheDocument();
    expect(screen.getByText('Test subtitle')).toBeInTheDocument();
  });
  
  it('renders trend indicator when provided', () => {
    render(
      <KPICard 
        title="METRIC" 
        value={100}
        trend={{ direction: 'up', percentage: 10, period: 'daily' }}
      />
    );
    
    expect(screen.getByText('10%')).toBeInTheDocument();
    expect(screen.getByText('daily')).toBeInTheDocument();
  });
  
  it('renders KPI grid with multiple cards', () => {
    render(<KPIGrid />);
    
    expect(screen.getByText('OPEN ROLES')).toBeInTheDocument();
    expect(screen.getByText('CANDIDATES FOUND')).toBeInTheDocument();
  });
});


describe('Agent Control Center', () => {
  it('renders agent status badge', () => {
    render(<AgentStatusBadge status="running" />);
    
    expect(screen.getByText(/Running/i)).toBeInTheDocument();
  });
  
  it('renders agent control center with agents', () => {
    render(<AgentControlCenter />);
    
    expect(screen.getByText('Agent Control Center')).toBeInTheDocument();
  });
});


describe('Autonomy Mode Selector', () => {
  beforeEach(() => {
    localStorage.clear();
  });
  
  it('renders all autonomy levels', () => {
    render(<AutonomyModeSelector />);
    
    expect(screen.getByText('Advise')).toBeInTheDocument();
    expect(screen.getByText('Approve')).toBeInTheDocument();
    expect(screen.getByText('Semi')).toBeInTheDocument();
    expect(screen.getByText('Auto')).toBeInTheDocument();
  });
  
  it('defaults to L2 mode', () => {
    render(<AutonomyModeSelector />);
    
    const approveButton = screen.getByRole('button', { name: /Approve/ });
    expect(approveButton).toHaveClass('ring-2');
  });
});
