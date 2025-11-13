'use client';

import { useEffect, useState } from 'react';
import {
  ArrowUpRight,
  PlusCircle,
  QrCode,
  Users,
  Wallet,
} from 'lucide-react';

import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import Link from 'next/link';
import { Badge } from '@/components/ui/badge';
import { credentialsService, connectionsService, proofsService } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';

interface DashboardStats {
  totalCredentials: number;
  activeConnections: number;
  pendingRequests: number;
  recentActivityCount: number;
}

export default function DashboardPage() {
  const { toast } = useToast();
  const [stats, setStats] = useState<DashboardStats>({
    totalCredentials: 0,
    activeConnections: 0,
    pendingRequests: 0,
    recentActivityCount: 0,
  });
  const [loading, setLoading] = useState(true);
  const [recentActivities] = useState([
    { type: 'Credential Received', details: 'University Degree from MIT', time: '2h ago', status: 'Success'},
    { type: 'Proof Sent', details: 'Age Verification to SocialApp', time: '5h ago', status: 'Success'},
    { type: 'Connection Established', details: 'Connected with Tech Corp', time: '1d ago', status: 'Success'},
    { type: 'Proof Request', details: 'From GovPortal for ID check', time: '2d ago', status: 'Pending'},
  ]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch data in parallel
      const [credentialsCount, activeConnsCount, pendingProofsCount] = await Promise.all([
        credentialsService.getCredentialsCount().catch(() => 0),
        connectionsService.getActiveConnectionsCount().catch(() => 0),
        proofsService.getPendingProofRequestsCount().catch(() => 0),
      ]);

      setStats({
        totalCredentials: credentialsCount,
        activeConnections: activeConnsCount,
        pendingRequests: pendingProofsCount,
        recentActivityCount: credentialsCount + activeConnsCount,
      });
    } catch (error: any) {
      console.error('Failed to fetch dashboard data:', error);
      toast({
        title: 'Failed to load dashboard data',
        description: error.message || 'Please try refreshing the page',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="flex flex-col gap-6">
      <div className="grid gap-4 md:grid-cols-2 md:gap-8 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Total Credentials
            </CardTitle>
            <Wallet className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {loading ? '...' : stats.totalCredentials}
            </div>
            <p className="text-xs text-muted-foreground">
              Stored in your wallet
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Active Connections
            </CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {loading ? '...' : stats.activeConnections}
            </div>
            <p className="text-xs text-muted-foreground">
              Established connections
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pending Requests</CardTitle>
            <QrCode className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {loading ? '...' : stats.pendingRequests}
            </div>
            <p className="text-xs text-muted-foreground">
              Proof requests awaiting action
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Recent Activity</CardTitle>
            <PlusCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {loading ? '...' : stats.recentActivityCount}
            </div>
            <p className="text-xs text-muted-foreground">
              Total items in wallet
            </p>
          </CardContent>
        </Card>
      </div>
      <div className="grid gap-4 md:gap-8 lg:grid-cols-2 xl:grid-cols-3">
        <Card className="xl:col-span-2">
          <CardHeader className="flex flex-row items-center">
            <div className="grid gap-2">
              <CardTitle>Recent Activity</CardTitle>
              <CardDescription>
                An overview of your recent wallet events.
              </CardDescription>
            </div>
            <Button asChild size="sm" className="ml-auto gap-1">
              <Link href="#">
                View All
                <ArrowUpRight className="h-4 w-4" />
              </Link>
            </Button>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Event</TableHead>
                  <TableHead>Details</TableHead>
                  <TableHead className="text-right">Time</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {recentActivities.map((activity, index) => (
                    <TableRow key={index}>
                    <TableCell>
                        <div className="font-medium">{activity.type}</div>
                        <Badge variant={activity.status === 'Success' ? 'secondary' : 'outline'} className="mt-1 bg-accent/50 text-accent-foreground">{activity.status}</Badge>
                    </TableCell>
                    <TableCell>{activity.details}</TableCell>
                    <TableCell className="text-right">{activity.time}</TableCell>
                    </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>Perform common tasks with a single click.</CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4">
              <Button>
                <QrCode className="mr-2 h-4 w-4"/>
                Scan QR Code
              </Button>
              <Button variant="secondary" asChild>
                <Link href="/dashboard/credentials">
                    <Wallet className="mr-2 h-4 w-4" />
                    View All Credentials
                </Link>
              </Button>
              <Button variant="secondary" asChild>
                <Link href="/dashboard/connections">
                    <Users className="mr-2 h-4 w-4" />
                    Manage Connections
                </Link>
              </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
