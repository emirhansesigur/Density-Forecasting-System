namespace Application.SpecialDays.Models;
public class SpecialDayRequestModel
{
    public string Name { get; set; }
    public DateOnly Date { get; set; }
    public string? Description { get; set; }
}
