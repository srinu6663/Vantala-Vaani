import { useState, useEffect } from "react";
import { useLocation } from "wouter";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { UploadModal } from "@/components/upload-modal";
import { useTheme } from "@/components/theme-provider";
import { useNotification } from "@/components/notification";
import { getUserContributions, getCurrentUser } from "@/lib/api";
import { getAuthToken, removeAuthToken } from "@/lib/auth";
import { Database, Upload, FileText, Mic, Video, Images, Moon, Sun, LogOut, Plus, MoreVertical } from "lucide-react";
import type { Contribution } from "@shared/schema";


export default function DashboardPage() {
  const [, setLocation] = useLocation();
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [userId, setUserId] = useState<string | null>(null);
  const [userName, setUserName] = useState<string>('User');
  const { theme, toggleTheme } = useTheme();
  const { showNotification } = useNotification();
  const queryClient = useQueryClient();

  useEffect(() => {
    const token = getAuthToken();
    const userId = sessionStorage.getItem('userId');
    if (!token || !userId) {
      setLocation('/');
      return;
    }
    setUserId(userId);
    // Fetch user name from API
    getCurrentUser()
      .then((user) => {
        setUserName(user.name || 'User');
      })
      .catch(() => setUserName('User'));
  }, [setLocation]);

  const { data: contribData, isLoading } = useQuery({
    queryKey: ['/api/v1/users', userId, 'contributions'],
    queryFn: () => userId ? getUserContributions(userId) : Promise.resolve(null),
    enabled: !!userId,
  });

  const handleLogout = () => {
    removeAuthToken();
    sessionStorage.removeItem('userId');
    queryClient.clear();
    showNotification('Info', 'You have been logged out', 'info');
    setLocation('/');
  };

  const getContributionIcon = (type: string) => {
    switch (type) {
      case 'text': return <FileText className="h-5 w-5 text-primary" />;
      case 'audio': return <Mic className="h-5 w-5 text-secondary" />;
      case 'video': return <Video className="h-5 w-5 text-accent-foreground" />;
      case 'image': return <Images className="h-5 w-5 text-muted-foreground" />;
      default: return <FileText className="h-5 w-5 text-primary" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'approved': return 'bg-primary/10 text-primary';
      case 'processing': return 'bg-muted text-muted-foreground';
      case 'rejected': return 'bg-destructive/10 text-destructive';
      default: return 'bg-muted text-muted-foreground';
    }
  };

  // New API returns structured object, so stats are direct
  const stats = {
    total: contribData?.total_contributions || 0,
    text: contribData?.contributions_by_media_type?.text || 0,
    audio: contribData?.contributions_by_media_type?.audio || 0,
    video: contribData?.contributions_by_media_type?.video || 0,
    image: contribData?.contributions_by_media_type?.image || 0,
  };

  if (!userId) {
    return <div className="min-h-screen bg-background" />;
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-card shadow-sm border-b border-border sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center text-xl">
                <span role="img" aria-label="logo">🍽️</span>
              </div>
              <h1 className="text-xl font-semibold text-card-foreground">Vantala Vaani</h1>
            </div>

            <div className="flex items-center space-x-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={toggleTheme}
                data-testid="button-theme-toggle"
                className="text-muted-foreground hover:text-foreground"
              >
                {theme === 'dark' ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
              </Button>
              <Button
                onClick={() => setShowUploadModal(true)}
                className="bg-primary text-primary-foreground hover:bg-primary/90"
                size="sm"
                data-testid="button-navbar-upload"
                title="Upload Contribution"
              >
                <Upload className="mr-2 h-4 w-4" />
                Upload
              </Button>
              <div className="flex items-center space-x-2 text-card-foreground">
                <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                  <span className="text-primary-foreground text-lg font-bold">
                    {userName ? userName.charAt(0).toUpperCase() : '?'}
                  </span>
                </div>
                <span className="font-medium">
                  {userName}
                </span>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={handleLogout}
                data-testid="button-logout"
                className="text-muted-foreground hover:text-destructive"
              >
                <LogOut className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Dashboard Overview */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-card-foreground mb-2">Welcome back!</h2>
          <p className="text-muted-foreground">Manage your contributions and upload new content</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-8">
          <Card className="border-border">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-muted-foreground text-sm">Total Contributions</p>
                  <p className="text-2xl font-bold text-card-foreground" data-testid="stats-total">
                    {stats.total}
                  </p>
                </div>
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                  <Upload className="text-primary h-5 w-5" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-border">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-muted-foreground text-sm">Text Records</p>
                  <p className="text-2xl font-bold text-card-foreground" data-testid="stats-text">
                    {stats.text}
                  </p>
                </div>
                <div className="w-12 h-12 bg-secondary/10 rounded-lg flex items-center justify-center">
                  <FileText className="text-secondary h-5 w-5" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-border">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-muted-foreground text-sm">Audio Files</p>
                  <p className="text-2xl font-bold text-card-foreground" data-testid="stats-audio">
                    {stats.audio}
                  </p>
                </div>
                <div className="w-12 h-12 bg-accent rounded-lg flex items-center justify-center">
                  <Mic className="text-accent-foreground h-5 w-5" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-border">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-muted-foreground text-sm">Video Files</p>
                  <p className="text-2xl font-bold text-card-foreground" data-testid="stats-video">
                    {stats.video}
                  </p>
                </div>
                <div className="w-12 h-12 bg-muted rounded-lg flex items-center justify-center">
                  <Video className="text-muted-foreground h-5 w-5" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-border">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-muted-foreground text-sm">Images</p>
                  <p className="text-2xl font-bold text-card-foreground" data-testid="stats-images">
                    {stats.image}
                  </p>
                </div>
                <div className="w-12 h-12 bg-muted rounded-lg flex items-center justify-center">
                  <Images className="text-muted-foreground h-5 w-5" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Action Buttons */}
        <div className="mb-8">
          <Button
            onClick={() => setShowUploadModal(true)}
            className="bg-primary text-primary-foreground hover:bg-primary/90"
            data-testid="button-new-contribution"
          >
            <Plus className="mr-2 h-4 w-4" />
            New Contribution
          </Button>
        </div>

        {/* Recent Contributions */}
        <Card className="border-border">
          <CardContent className="p-6">
            <div className="border-b border-border pb-4 mb-4">
              <h3 className="text-xl font-semibold text-card-foreground">Recent Contributions</h3>
              <p className="text-muted-foreground">Your latest uploads and submissions</p>
            </div>

            {isLoading ? (
              <div className="space-y-4">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="flex items-center space-x-4">
                    <Skeleton className="w-10 h-10 rounded-lg" />
                    <div className="flex-1">
                      <Skeleton className="h-4 w-48 mb-2" />
                      <Skeleton className="h-3 w-32" />
                    </div>
                    <Skeleton className="h-6 w-20 rounded-full" />
                  </div>
                ))}
              </div>
            ) : (() => {
              if (contribData) {
                const allContributions = [
                  ...(contribData.text_contributions || []),
                  ...(contribData.audio_contributions || []),
                  ...(contribData.image_contributions || []),
                  ...(contribData.video_contributions || []),
                ];
                allContributions.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
                if (allContributions.length > 0) {
                  return (
                    <div className="space-y-4">
                      {allContributions.slice(0, 5).map((contribution) => (
                        <div
                          key={contribution.id}
                          className="flex items-center justify-between p-4 hover:bg-accent/50 rounded-lg transition-colors"
                          data-testid={`contribution-${contribution.id}`}
                        >
                          <div className="flex items-center space-x-4">
                            <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                              {getContributionIcon(contribution.type || contribution.media_type || 'text')}
                            </div>
                            <div>
                              <h4 className="font-medium text-card-foreground">{contribution.title}</h4>
                              <p className="text-sm text-muted-foreground">
                                {(contribution.type || contribution.media_type || 'text').charAt(0).toUpperCase() + (contribution.type || contribution.media_type || 'text').slice(1)} • {' '}
                                {contribution.timestamp ? new Date(contribution.timestamp).toLocaleDateString() : 'Recently'}
                              </p>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(contribution.status || (contribution.reviewed ? 'approved' : 'processing'))}`}>
                              {(contribution.status || (contribution.reviewed ? 'approved' : 'processing')).charAt(0).toUpperCase() + (contribution.status || (contribution.reviewed ? 'approved' : 'processing')).slice(1)}
                            </span>
                            <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-foreground">
                              <MoreVertical className="h-4 w-4" />
                            </Button>
                          </div>
                        </div>
                      ))}
                      {allContributions.length > 5 && (
                        <div className="pt-4 border-t border-border">
                          <Button variant="ghost" className="text-primary hover:text-primary/80 font-medium text-sm">
                            View All Contributions →
                          </Button>
                        </div>
                      )}
                    </div>
                  );
                }
              }
              // Fallback: No contributions
              return (
                <div className="text-center py-8">
                  <Upload className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
                  <h4 className="text-lg font-medium text-card-foreground mb-2">No contributions yet</h4>
                  <p className="text-muted-foreground mb-4">Start by uploading your first contribution</p>
                  <Button
                    onClick={() => setShowUploadModal(true)}
                    className="bg-primary text-primary-foreground hover:bg-primary/90"
                  >
                    <Plus className="mr-2 h-4 w-4" />
                    Create Contribution
                  </Button>
                </div>
              );
            })()}
          </CardContent>
        </Card>
      </div>

      {/* Upload Modal */}
      <UploadModal
        open={showUploadModal}
        onOpenChange={setShowUploadModal}
        userId={userId}
      />
    </div>
  );
}
